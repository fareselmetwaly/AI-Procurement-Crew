from pathlib import Path
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
import crew_project.core.configurations as configurations


class EvaluationVerdict(BaseModel):
    approved: bool = Field(..., description="True if the report passes all criteria, False otherwise.")
    feedback: str = Field(..., description="Specific fixes required if not approved, or 'None' if approved.")


def run_evaluator_loop(config: dict, report_path: Path, max_iterations: int) -> None:
    """Evaluates the generated HTML report and refines it up to max_iterations times."""
    if not report_path.exists():
        return

    groq_llm = configurations.groq_llm  # نقرا الـ LLM الحالي وقت التشغيل (بعد أي تغيير من Settings)

    evaluator_agent = Agent(
        role="Procurement Report Quality Evaluator",
        goal="Strictly verify that the HTML report matches every currency, date, budget, and spec constraint.",
        backstory="Senior procurement auditor ensuring zero inaccuracies before executive delivery.",
        llm=groq_llm,
        verbose=True,
    )

    optimizer_agent = Agent(
        role="Procurement Report Optimizer",
        goal="Fix every issue flagged by the evaluator while preserving clean raw HTML output.",
        backstory="Expert HTML report editor refining procurement documents based on audit feedback.",
        llm=groq_llm,
        verbose=True,
    )

    for attempt in range(1, max_iterations + 1):
        current_html = report_path.read_text(encoding="utf-8")

        eval_task = Task(
            description="\n".join([
                f"Audit this HTML procurement report (Attempt {attempt}/{max_iterations}):",
                f"- Required Currency: {config.get('currency')}",
                f"- Required Exact Date: {config.get('full_date')}",
                f"- Budget: {config.get('budget_text')}",
                f"- Important Specs: {config.get('important_specs_text')}",
                f"- Brand Rule: {config.get('israeli_filter_rule')}",
                f"HTML Content:\n{current_html}",
            ]),
            expected_output="JSON verdict with 'approved' boolean and actionable 'feedback'.",
            output_json=EvaluationVerdict,
            agent=evaluator_agent,
        )

        eval_crew = Crew(agents=[evaluator_agent], tasks=[eval_task], process=Process.sequential)
        eval_res = eval_crew.kickoff()
        verdict = eval_res.json_dict or {}

        if verdict.get("approved"):
            break

        fix_task = Task(
            description="\n".join([
                "Update the following HTML report to fix all issues listed in the audit feedback.",
                f"Audit Feedback:\n{verdict.get('feedback')}",
                "Output ONLY raw HTML starting with <!DOCTYPE html> and ending with </html>.",
                f"Current HTML:\n{current_html}",
            ]),
            expected_output="Corrected raw HTML document.",
            output_file=str(report_path),
            agent=optimizer_agent,
        )

        fix_crew = Crew(agents=[optimizer_agent], tasks=[fix_task], process=Process.sequential)
        fix_crew.kickoff()