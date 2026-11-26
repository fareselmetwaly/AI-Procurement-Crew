# AI-Powered Procurement Research & Decision Support System

## Business Problem

When a company needs to purchase a product, identifying suitable options requires researching multiple websites and suppliers, collecting product information, verifying specifications, and comparing available offers.

Traditional procurement research often involves significant manual effort, fragmented information, and inconsistent data collection, making it difficult to evaluate alternatives efficiently and make well-informed purchasing decisions.

The main challenges include:

- **Time-Consuming Research:** Spending considerable time searching across multiple websites and suppliers.
- **Fragmented Information:** Product details, prices, and specifications are scattered across different sources.
- **Manual Data Collection:** Gathering and organizing product information requires repetitive manual work.
- **Incomplete or Inconsistent Data:** Some product listings may lack essential information or contain unclear details.
- **Complex Decision-Making:** Comparing alternatives across multiple criteria makes identifying suitable purchasing options more difficult.

This project addresses these challenges by automating procurement research and organizing structured, source-backed product information to support better purchasing decisions.

## Project Objectives

The primary objective of this project is to automate procurement research and transform scattered product information into structured insights that help businesses make informed purchasing decisions.

The system aims to:

1. **Automate Procurement Research:** Reduce manual effort by searching for relevant products across multiple websites and suppliers.
2. **Centralize Product Information:** Collect and organize product details, specifications, pricing, and supplier information in a unified structure.
3. **Improve Data Reliability:** Validate collected information, preserve source references, and explicitly identify missing or uncertain data.
4. **Facilitate Product Evaluation:** Assess available alternatives against the company's purchasing requirements and comparison criteria.
5. **Generate Comprehensive Reports:** Present research findings, product comparisons, observations, and recommendations in a professional report.
6. **Support Informed Decision-Making:** Provide management with structured insights while keeping the final purchasing decision under human control.

**Decision Ownership:** The system supports research, evaluation, and recommendations. It does not independently make or execute purchasing decisions.

## Key Features

- **Purchase Requirement Definition:** Allows users to specify the required product, quantity, specifications, and purchasing criteria.
- **Flexible Research Scope:** Supports searching within user-defined websites and suppliers or discovering additional sources through open research.
- **AI-Powered Search Query Generation:** Generates relevant search queries based on the purchasing requirements.
- **Human-in-the-Loop Search Approval:** Allows users to review, modify, and approve AI-generated search queries before the research process begins.
- **Automated Product Research:** Searches across selected or discovered sources to identify relevant products and available offers.
- **Product Data Extraction:** Collects and structures product details, specifications, pricing, and supplier information.
- **Data Validation & Filtering:** Evaluates the relevance and completeness of collected information, separating qualified results from items requiring further review.
- **Product Evaluation & Comparison:** Analyzes available alternatives against the company's requirements and presents comparative insights.
- **Research-Based Recommendations:** Provides observations and recommendations supported by collected product data.
- **Comprehensive Report Generation:** Produces a professional report containing research findings, product comparisons, recommendations, and additional results requiring review.

## How It Works

The system follows a structured procurement research workflow:

1. **Purchase Request:** The user provides the product requirements, including relevant specifications and purchasing criteria.
2. **Research Scope Selection:** The user specifies target websites or suppliers, or allows the system to discover relevant sources independently.
3. **Search Query Generation:** The AI generates suggested search queries based on the provided requirements.
4. **Human Review & Approval:** The user reviews and modifies the suggested queries if necessary, then approves them before research begins.
5. **Automated Research:** The system searches the selected or discovered sources and collects relevant product results.
6. **Data Extraction & Validation:** Product information is extracted, structured, and checked for relevance, completeness, and reliability.
7. **Evaluation & Comparison:** Qualified alternatives are evaluated and compared against the company's purchasing requirements.
8. **Final Report Generation:** The system generates a structured report containing the main research findings, comparisons, observations, and recommendations.

Products with relevant information but missing or uncertain details are retained separately in an additional research section for management review rather than being silently discarded.

## Expected Outcomes

The system aims to provide businesses with:

- Reduced time and manual effort spent on procurement research.
- Centralized and structured product information from multiple sources.
- Improved visibility into available purchasing alternatives.
- Clearer comparisons based on the company's requirements.
- Traceable product information supported by source references.
- Identification of missing information and products requiring further review.
- Professional procurement research reports that support informed management decisions.

The final report serves as a decision-support resource, enabling management to review available alternatives and determine the most appropriate purchasing action.



دلوقتي فكرة البروجكت اللي أنا شغال عليها إن أنا شركة معينة وعندي عايز أشتري منتج معين، وبالتالي أنا عندي شخص مسؤول مبيعات، بديله المنتج اللي أنا عايزه، بيبدأ هو يبحث على مواقع معينة ممكن أنا بحددها له أو هو بيفضل يبحث عنها عشان يطلع لي أفضل نتائج مقابل سعر، يطلع الملاحظات بتاعتها، التوصيات، كل حاجة. بعد كده في النهاية يطلع لي فاينل ريبورت، بناء عليه بناخد اكشن كشركة. ده فكرة البروجكت، تمام؟ طيب بعد كده هنبدأ نشوف الفلو اللي بيمشي بيها البروجكت.


دلوقتي الفلو بتاع الايجنتيك اي هيمشي كالتالي. مبدئيا هو هيمشي سيكونشال بالتتابع، واحنا عندنا السيستم بتاع الايجنت هينقسم ل4 ايجنت. اول ايجنت بيبدا هيكون وظيفته او التاسك بتاعته ان انا بقول له على منتج معين او حاجه معينه، هو يبدا يطلع لي زي مجموعه من الحاجات اللي ممكن ابحث بيها، الاقتراحات يعني هبحث بيها على السيرش انجن. فيبقى الاوتبوت اللي يطلع من الايجنت الاولاني هيكون list of keywords suggested. بعد كده باجي للايجنت الثاني بياخد الليست اللي انا اديتها له من الايجنت الاول، يبدا ان هو يسيرش عن الاقتراحات اللي هو خدها من الايجنت الاولاني، بالاضافه ان انا بديله تول يسيرش بيها. بعد ما بيخلص الايجنت الثاني ويطلع لي النتائج اللي انا عايزها، بيطلع لي مجموعه من النتائج. ببدا النتائج دي ببصيها للايجنت الثالث عشان يكستراكت البرودكت او الحاجات منها ويطلع لي التفاصيل بتاعتها. وبنستخدم في الحاله دي ممكن HTML parser كودينج او تول. بعد كده الايجنت ده رقم 3 بيطلع لي structure details عن المنتجات اللي هو طلعها لي. بعد ما طلع لي الديتيلز بتاعت المنتجات من كذا مكان والتفاصيل بتاعتها وكل حاجة، ببدأ ان انا اشوف عشان اعمل جينيريشن لتقرير مبيعات محترم. وفي الحالة دي انا ممكن استخدم تول ان هي تجنريت ال HTML، او ان انا اعتمد على الموديل بيكون نيتف ان انا اقدر هولد منه HTML عشان في النهاية يطلع لي باوتبوت فيجوال فاينل ريبورت بروفيشنال. اقدر ان انا اديه للاداره او الشركه تاخد بناء عليه قرار.



طيب بالنسبة للسيرش بقى، فالمفروض ان انا احاول اظبط في البرومبت ان هو يدور على منتجات لا تدعم الكيان الصهيوني ولا تدعم اي شركات تبع الكيان الصهيوني، بالاضافة ان انا هنشر الاداة اللي بتاعت احمد حسنين اللي هي ذا وول، اللي بتكتشف لنا 20,000 شركة إسرائيلية أو تابعين ليها. اللي أنا عايز أعمله




طيب المفروض ان انا في جزء هقسمه البيزنس او بيحكي عن المشكله اللي انا بحلها، جزء تاني بيتكلم عن التكنيكال وازاي نفذته وكده. تمام. طيب المشروع هيكون فيه سيكونشال ايجنت، 4 ايجنت ورا بعض زي ما احنا عارفين، بالاضافه لان دي حاجه هتبقى اختياريه، ممكن نفعلها وممكن لا، اللي هي الايفالويتر اوبتمايزر باترن، ديزاين باترن يعني ممكن نستخدمها بحيث انه يتشيك على الحاجه اللي طلعت تمام مش تمام، لو مش تمام بيدي فيدباك ويرجع يعمل زي لوب تاني وهكذا.



طيب بالإضافة لإيه؟ آه،