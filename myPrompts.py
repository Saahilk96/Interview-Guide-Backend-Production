def company_research_fun(data):
    company_research = (f'''
    You are an expert research assistant helping a user prepare for a job interview.
Your task is to identify the company, research it thoroughly, and generate a detailed JSON output containing key information relevant for interview preparation.
    {data}'''
    '''
    ----

*INSTRUCTIONS:*

1. Identify Company:
    - Start with the 'COMPANY NAME' provided in the input as the primary candidate.
    - **Crucially, use the 'COMPANY WEBSITE' (if available in the input) to disambiguate this name.** Analyze its domain to distinguish this specific company from others that might share a similar name. This step is vital for pinpointing the exact entity the user is referring to.
    - Further refine and confirm the specific company identity by analyzing the 'JOB DESCRIPTION'. Look for contextual clues (industry, services mentioned, specific technologies, location if relevant) that align with the website information and the provided company name, helping to resolve any remaining ambiguity.
    - Your objective is to accurately determine and confirm the single, specific company entity intended by the user for subsequent research.

Research: **Using the identified company name, leverage your general knowledge base for a foundational understanding of the company (e.g., its industry, general product categories, common perceptions). However, to ensure the highest accuracy and up-to-date information for specific factual and potentially time-sensitive details, you **must prioritize and actively employ your searching grounding (searching the internet) capabilities.** Aim for comprehensive information, using search to validate, update, or find details that are likely to be current or highly specific.This approach is especially critical for gathering precise information on:

- Mission & Values
- Founding Team - Company founding date & Key founder(s)
- Products & Services
- Business Model & Market Footprint
- Recent funding rounds (including amounts, dates, and key investors, if publicly available)
- Key recent events (e.g., significant news, major product launches, acquisitions, strategic partnerships, ideally within the last 1-2 years)
- Current key leadership roles and names (e.g., CEO, CPO, CTO)
- Specific financial details (e.g., revenue trends if public, latest valuation if reported)
- Notable clients/customers (verifying publicly acknowledged relationships)

-----

REQUIRED INFORMATION CATEGORIES (Map these to the JSON structure):

- ***Quick Summary:*** High-impact overview (~2 mins) covering: What the company does, its primary product/service, key customer segment & problem solved & company's advantage
- **Company Overview:**
    - **Company Snapshot:** 3–4 sentence summary explaining what the company does, its core product or service, key innovation, and why it matters in its industry
    - **Mission & Values: Instruction - This information should not be inferred or guessed, it should be searched on the web for the most accurate result**
        - Mission: 1 sentence stating the mission statement of the company, if available
        - Vision: 1 sentence stating the vision statement of the company, if available
        - Values/Principles: List all the values/principles of the company, if available
    - **Founding Team:** String (In 1-2 sentences, state the *year* company_name was founded and list *all the names* *e.g. name(job title)* of its founders entirely from web search) e.g. *The founders of company_name are name1(job title), name2(job title), name3(job title),etc.*
- **Products & Services: Instruction:** - Your primary task here is to thoroughly search the web, especially the company's official website (navigating their "Products," "Services," "Solutions," or equivalent sections), to identify and list all of the company's *main, distinct* products and/or service lines.
    - **Distinguishing Main Products from Features:** If a company offers a primary product that has many features or sub-components, list the *main product* as the offering. Only list sub-components or features as separate "Product/Service" entries if the company markets and presents them as distinct, standalone offerings. The goal is to reflect how the company categorizes and presents its offerings to the market.
    - **Handling Numerous Offerings:** For companies with an extensive portfolio of many distinct products/services, strive to list all *major* or *primary* offerings. If the list becomes exceptionally long (e.g., dozens of minor variations), prioritize those that appear most strategically important, are highlighted by the company, or (if a job description is part of the input) are most relevant to the role. However, the initial goal should be to capture the breadth of their main offerings.
    - **Description:** For each distinct product or service identified, provide its name followed by a concise 1-2 line description detailing what it is and its core function or benefit.
    - **Source Verification:** This information MUST be actively searched and verified online. Prioritize the company's official website and reputable industry sources. Do not rely solely on general knowledge, as product portfolios change.
    Example Format (to be followed for each entry in the JSON subPoints):
    - [Product/Service Name 1:** [Concise 1-2 sentence description of Product/Service 1.]
    - [Product/Service Name 2:** [Concise 1-2 sentence description of Product/Service 2.] ad keep repeat for all offerings found
- **Business Model & Company Financials:**
    - **Business Model & Monetization: 1- 3 points outlining what is the b primary business model of the company**
    - **- **Financials & Funding: Instructions for Research and Formatting:**
    - **General Goal:** Provide a concise overview of the company's recent funding history. All information must be sourced from reliable web searches.
    - **For Privately Held Companies:**
        - **Objective:** Provide a comprehensive list of funding rounds, with a primary focus on the last 5 years, and also capturing essential earlier rounds if funding history is sparse.
        - **Instruction:** Actively search for all known funding rounds.
            - **Your primary goal is to list ALL distinct funding rounds announced in the past 5 years.** For each round, include its type (e.g., Seed, Series A, Pre-seed), amount, date (Month/Year or Q#/Year), and key/lead investors. Include all rounds found within this 5-year period, regardless of how many there are.
            - **Additionally, if the company has had very few funding rounds in total (e.g., only 1-2 rounds ever) and these foundational rounds are older than 5 years, ensure these are also listed.** The aim is to provide a complete funding picture where possible.
        - **Example for a subPoint string (to be used for each funding round listed in the JSON `subPoints`):** "Series C - $120M - May 2023 - led by Sequoia, participation from Accel."
    - **For Publicly Traded Companies (e.g., those that have had an IPO):**
        - **First subPoint string should typically state:** The company's public status, its stock ticker, the exchange it trades on, and its IPO date and key details (e.g., "Went public via IPO on NASDAQ (Ticker: GOOGL) on August 19, 2004, raising $1.67 billion.").
        - **Subsequent subPoint strings (if applicable and significant recent events exist):** Detail any major post-IPO financing events like significant secondary offerings, large debt financing rounds, or major investments received. If no such recent, distinct "funding rounds" exist post-IPO, this can be briefly stated, or the IPO information might be the primary focus for funding history.
        - **Avoid generic placeholders.** If specific post-IPO funding events aren't prominent, focus on the IPO details and current public market funding.
    - **Formatting in JSON:** Each piece of funding information (whether a private round or a public company detail) should be a single string within the `subPoints` array for "Financials & Funding".
    - **Revenue:** List the most up to date revenue available of the company. Do not guess this number, if its not publicly available then mention as such. For companies that are public this number should be easily available. If the company is private focus on reputable news sources.
- **Target Market & Customers:**
    - Primary Customer Segments: Provide a 3-5 sentence summary of key industries, sectors or target market that the company serves, if they serve multiple industries then focus on the main industry they serve with the product mentioned in the job description. A
    - Key Customer Challenges Solved: Problems/needs addressed by products/services.
    - Key Reasons Customers Choose: Top 2-3 USPs/differentiators.
    - Notable Clients: 5-7 significant clients that the company has worked with (publicly known)
- **Competitive Landscape:**
    - Main Competitors: List 5-7 significant competitors. These can be direct or indirect competitors
    - Key Differentiators (USPs): 1-3 points making the differentiates the company from its competitors. Focus on the things that the company does that sets it apart from its competitors and is the reason companies prefer the company over the competitors
    - Competitive Strengths: 1-3 core advantages (e.g., technology, brand).
    - Potential Weaknesses/Challenges: 1-3 potential vulnerabilities relative to competitors.
- **Organization Structure & Leadership:**
    - Size, Status & Location: Approx Employee Count, Public/Private, HQ, Key Offices.
    - Organizational Structure: Parent Company, Key Subsidiaries/Divisions, recent restructuring.
    - Key Leadership: CEO, CPO/Product Head, CTO/Engineering Head, other relevant VPs/Heads (provide names).
- **Industry Context, News & Trends**
    - **Key Industry Trends:** List all the key trends in the company’s primary industry that the company
    - **Recent News & Key Developments:** 3-5 significant events from the last 5 years (funding, product launches, acquisitions, partnerships, milestones reached etc.). Summarize each factually in one sentence (e.g., "Acquired Company Y, expanding its market presence in Asia, in Q3 2023.")
    -----

    **The JSON Output should be in this format only and ensure atleast `2 subPoints` should,must be filled in each object of sub_modules and the 'completed' must be 'false' only:**
    {
  "quick_summary": "[A comprehensive 5–6 paragraph overview covering what the company does, its products/services, customer segments, problems solved, competitive advantage, recent momentum, and industry relevance.]",
  "sub_modules": [
    {
      "title": "Company Overview",
      "completed": false,
      "summary": "This module offers a concise yet comprehensive overview of the company, detailing its core operations, mission, values, and foundational history to provide a clear understanding of its identity and purpose.",
      "content": "Delve into the company's essence with a snapshot of its business, explore its guiding mission and core values, and discover the vision that drives its future. This section also introduces the pivotal individuals who founded the company, marking its origins.",
      "htmlContent": "<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Company Snapshot</h3>\
            <p class='mb-4 text-gray-300'>String (3–4 sentence summary explaining what the company does, core product/service, key innovation, and relevance)</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Mission & Values</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>Mission: string (Mission of the company. Must be sourced, not inferred.)</li>\
              <li>Vision: string (Vision of the company. Must be sourced, not inferred.)</li>\
              <li>Values/Principles: string, string, string (List of values/Principles; must be sourced, not inferred.)</li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Founding Team</h3>\
            <p class='text-gray-300'>String (In 1-2 sentences, state the year company_name was founded and list all the names e.g. name(job title) of its founders entirely from web search) e.g. The founders of company_name are name1(job title), name2(job title), name3(job title),etc.</p>\
          </div>"
    },
    {
      "title": "Products & Services",
      "completed": false,
      "summary": "This module provides an in-depth look at the company's diverse product and service offerings, highlighting their core functionalities and how they address specific customer needs. It offers a clear picture of the value proposition each offering brings to the market.",
      "content": "Explore the range of innovative products and essential services provided by the company. Understand their core functions, the specific benefits they offer to users, and how they collectively contribute to solving key market problems and delivering value.",
      "htmlContent": "<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Product & Service List</h3>\
            <ul class='list-none space-y-2 text-gray-300'>\
              <li><b>Product/Service A:</b> string (Concise 1-2 sentence description of what it is and does)</li>\
              <li><b>Product/Service B:</b> string (Same format, repeat as needed)</li>\
            </ul>\
          </div>"
    },
    {
      "title": "Business Model & Company Financials",
      "completed": false,
      "summary": "This module outlines the company's strategic approach to generating revenue, provides insights into its financial health, including recent funding rounds and public market status, and details its overall financial trajectory.",
      "content": "Discover how the company monetizes its offerings through a detailed look at its business model. This section also covers its funding history, including significant investment rounds or public market information, and provides an overview of its most recent revenue figures to give a complete financial picture.",
      "htmlContent": "<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Business Model & Monetization</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (e.g., 'Subscription-based SaaS platform for enterprise analytics')</li>\
              <li>String (e.g., 'Freemium pricing for individual users with tiered enterprise plans')</li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Financials & Funding</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (Detail of a specific funding event or relevant financial milestone. Examples: 'Series C – $120M – May 2023 – led by Sequoia' OR 'IPO: NASDAQ (TICKER) - Aug 2020, raised $500M' OR 'Post-IPO debt financing - $200M - Jan 2024')</li>\
              <li>String (Further funding details or milestones as applicable, following similar formats)</li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Revenue</h3>\
            <p class='text-gray-300'>Latest available revenue: string (e.g., '$210M in 2023' or 'Revenue not publicly available')</p>\
          </div>"
    },
    {
      "title": "Target Market & Customers",
      "completed": false,
      "summary": "This module clearly defines the company's target audience, detailing the specific segments it serves, the key challenges its products and services aim to resolve, and the distinct reasons why customers choose its solutions over alternatives.",
      "content": "Identify the primary customer segments that the company focuses on, understanding their unique needs and the core problems that the company's offerings are designed to solve. Learn about the compelling reasons and unique selling propositions that attract and retain its notable clients.",
      "htmlContent": "<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Primary Customer Segments</h3>\
            <p class='mb-4 text-gray-300'>String (3–5 sentences on key industries, sectors, or personas served)</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Key Customer Challenges Solved</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (List of core problems solved by the company’s products/services)</li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Key Reasons Customers Choose</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (1–2 sentence point on USP 1)</li>\
              <li>String (USP 2)</li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Notable Clients</h3>\
            <ul class='list-none space-y-1 text-gray-300'>\
              <li>Client 1</li>\
              <li>Client 2</li>\
            </ul>\
          </div>"
    },
    {
      "title": "Competitive Landscape",
      "completed": false,
      "summary": "This module provides a strategic overview of the company's competitive environment, identifying key rivals and outlining the critical differentiators that set the company apart, as well as potential weaknesses in the market.",
      "content": "Gain a clear understanding of the company's main competitors, both direct and indirect. This section highlights the unique selling propositions that differentiate the company in the market, its core competitive strengths, and any potential vulnerabilities or challenges it faces in relation to its rivals.",
      "htmlContent": "<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Main Competitors</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>Competitor A</li>\
              <li>Competitor B</li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Key Differentiators (USPs)</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (Point 1)</li>\
              <li>String (Point 2)</li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Competitive Strengths</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (e.g., 'Proprietary AI engine that automates analysis 30% faster')</li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Potential Weaknesses/Challenges</h3>\
            <ul class='list-none space-y-1 text-gray-300'>\
              <li>String (e.g., 'Limited geographic reach compared to global competitors')</li>\
            </ul>\
          </div>"
    },
    {
      "title": "Organization Structure & Leadership",
      "completed": false,
      "summary": "This module provides insights into the company's organizational framework, detailing its size, public or private status, key locations, and the hierarchical structure including its leadership team and significant divisions.",
      "content": "Understand the company's scale and structure, from its approximate employee count and public/private status to its headquarters and key global offices. This section also outlines its organizational hierarchy, including any parent companies or subsidiaries, and introduces the vital members of its leadership team.",
      "htmlContent": "<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Size, Status & Location</h3>\
            <p class='mb-4 text-gray-300'>String (e.g., 'Approx 1,500 employees, private company, HQ in San Francisco, regional offices in London and Bangalore')</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Organizational Structure</h3>\
            <p class='mb-4 text-gray-300'>String (e.g., 'Wholly-owned subsidiary of XYZ Group, with 3 business divisions: Consumer, Enterprise, Research')</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Key Leadership</h3>\
            <ul class='list-none space-y-1 text-gray-300'>\
              <li>CEO: Full Name</li>\
              <li>CPO: Full Name</li>\
              <li>CTO: Full Name</li>\
              <li>Other Key Heads: Role – Name</li>\
            </ul>\
          </div>"
    },
    {
      "title": "Industry Context, News & Trends",
      "completed": false,
      "summary": "This module provides essential context by highlighting prevalent trends within the company's industry and detailing recent news and significant developments that have shaped its trajectory and market position.",
      "content": "Explore the broader industry landscape affecting the company, including key trends that are driving change and innovation. This section also covers recent news and pivotal developments, such as major product launches, strategic partnerships, or acquisitions, that demonstrate the company's response to or influence on these trends.",
      "htmlContent": "<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Key Industry Trends</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>Trend 1</li>\
              <li>Trend 2</li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Recent News & Key Developments</h3>\
            <ul class='list-none space-y-1 text-gray-300'>\
              <li>Event 1: string (e.g., 'Acquired Company Y, expanding its market presence in Asia, in Q3 2023')</li>\
              <li>Event 2: string (Description of another significant event)</li>\
            </ul>\
          </div>"
    }
  ],
  "questions":"You are an expert interviewer. Your task is to generate relevant and insightful interview questions for a candidate applying for a [job_role] position at [company]. **IMPORTANT:** Do not generate any answers, only the questions. Please generate 5-7 distinct interview questions that cover a range of areas crucial for evaluating a candidate for this role. These should include: * **Company Knowledge & Alignment:** Questions that assess their understanding of [company]'s business model, mission, values, and how their aspirations align. * **Role-Specific Skills & Experience:** Questions tailored to the core responsibilities and technical or functional skills required for a [job_role]. * **Behavioral & Situational Scenarios:** Questions that uncover their problem-solving abilities, teamwork experience, leadership potential, and how they handle challenges or setbacks. * **Industry & Future Trends:** Questions about current trends, challenges, or the future direction of the industry relevant to [company] and the [job_role]'s field. Ensure all questions are open-ended, designed to encourage detailed and thoughtful responses. --- **Replace `[company]` with the actual company name** (e.g., \"Google\", \"Microsoft\", \"Tata Consultancy Services\") and **`[job_role]` with the specific job role** (e.g., \"Software Engineer\", \"Marketing Manager\", \"Data Scientist\")."
}
    ''')
    return company_research

def product_research_fun(data):
    product_research = (f'''
    You are an expert Researcher helping a user prepare for a job interview by analyzing a specific product.
Your task is to identify the primary product the candidate will be working on based on the Job Description (JD), company name and company website, research it thoroughly using primarily the provided company website, other official company sources, reputed website and your own knowledge base and generate a detailed JSON output containing key information relevant for interview preparation.
    {data} Description (JD)'''
    '''
    ----
    *INSTRUCTIONS:*

1. Identify Primary Focus Product:
    - Start by carefully reading the **'JOB DESCRIPTION (JD)'** provided in the input to identify ALL specific products, product lines, platforms, or teams mentioned (e.g., "Search", "Maps", "Assistant", "Cloud Platform").
    - Analyze the JD for **PM Responsibility Signals**: Look specifically within "Responsibilities", "What You'll Do", etc., for keywords indicating direct ownership or primary focus for the PM role (e.g., "own the roadmap for [Product X]", "define the strategy for [Product X]").
    - **Crucially, use the 'COMPANY Name or Company WEBSITE URL' (provided in the input) to confirm the existence and details of any product(s) identified from the JD.** This step is vital for pinpointing the exact product offering.
    - **Fallback Logic:** If no specific product is clearly identified for PM ownership in the JD, attempt to identify the company's main/flagship product relevant to the role from the **'COMPANY WEBSITE'**. If still unclear, identify the most relevant product category/business line from the website.
    - Your objective is to accurately determine and confirm the single, **Primary Focus Product** (or product category) for subsequent research. Other mentioned products can be considered **Contextual Products**.
2. Research Product Details: **Using the identified Primary Focus Product, conduct your deep research.**
    - **The 'COMPANY WEBSITE ' provided in the input is your ABSOLUTE PRIMARY AND AUTHORITATIVE SOURCE for all specific product details.** This includes its features, functionality, target audience, value proposition, and monetization.
    - You **MUST prioritize and actively use information directly from the provided 'COMPANY WEBSITE', official company sources (e.g., company blogs, official product documentation linked from the main website), reputable sources, and your knowledge base.** This ensures the highest accuracy and up-to-date information. Please ensure the information is as up-to-date as it can be.
    - **For information NOT typically found on a product page (e.g., names of direct competitors not mentioned by the company, broad market trends for SWOT analysis), you may supplement with your general knowledge or web searching capabilities, but clearly state if the information is not from the official company website.**

---

REQUIRED INFORMATION CATEGORIES (Map these to the JSON structure for the **Primary Focus Product**):

- ***Quick Summary (Product Focus):*** High-impact overview (at least 260 words) covering: What the [Primary Focus Product] does, its primary user segment & key problem solved, its unique value proposition & key differentiators.
- **Card 1: Product Overview:**
    - **What Core Product Does:** Clear, concise functional description.
    - **Primary Target Market Segment:** The specific market/industry category the product primarily serves.
    - **Key Problem(s) It Solves for Users:** Core pain points it addresses.
    - **Unique Value Proposition (UVP):** Its distinct promise and most significant benefit.
    - ** Key Differentiators:** Standout aspects setting it apart.
- **Card 2: Core Functionality:**
    - Identified Product Features & Descriptions: List all significant product features with a 1-2 line summary of what each does and its benefit.
    - Key Underlying Technology: Any specific tech fundamental to its performance or UVP.
    - Integration & Ecosystem Synergy: Critical integrations and how they enhance value.
    - Monetization Strategy & Pricing Approach: How the product generates revenue and its pricing model.
- **Card 3: User Focus & Core Needs:**
    - **Primary Target User Profile(s):** Detailed description of the main users.
    - **How Users Engage with the Product:** Common workflows or tasks.
    - **Fundamental User Needs Addressed:** Core 'jobs' or aspirations the product helps users fulfill.
- **Card 4: Competitive Landscape (Product-Focused):**
    - **Key Direct Competitors:** Who offers similar solutions?
    - **Indirect Competition & Alternative Solutions for the problem [Primary Focus Product] solves.**
    - **Positioning Against Competitors:** How it aims to win.
- **Card 5: SWOT Analysis:**
    - **Strengths:** Internal positives of the product.
    - **Weaknesses:** Internal negatives/limitations of the product.
    - **Opportunities:** External favorable factors for the product.
    - **Threats:** External negative conditions for the product.
    
    ---
    
    **The JSON Output should be in this format only and ensure atleast `2 subPoints` should,must be filled in each object of sub_modules and the 'completed' must be 'false' only:**
    {
    "quick_summary": "[A comprehensive 5–6 paragraph overview covering what the Primary Focus Product does, its key features, target users, problems solved, unique value proposition, differentiators, and its role within the company's ecosystem.]",
    "sub_modules": [
    {
    "title": "Product Overview",
    "completed": false,
    "summary": "This section provides a high-level overview of the product, detailing its core purpose, the main market it serves, the key problems it addresses for users, its unique value proposition, and what sets it apart from competitors. This summary is crucial for a quick understanding of the product's fundamental identity and market position.",
    "content": "Delve into the foundational aspects of the product, understanding its primary function, the specific market segment it targets, and the essential problems it aims to solve. This card also highlights the product's unique value proposition and key differentiators that make it stand out in the competitive landscape, emphasizing information derived directly from official company sources.",
    "htmlContent": "<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>What Core Product Does</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (Concise overview of the product's primary function and capabilities, e.g., 'An advanced analytics platform for processing and visualizing large datasets.') </li>\
              <li>String (The main activity or process it enables for users, according to the company website.) </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Primary Target Market Segment</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (The specific market or industry category the product primarily serves, e.g., 'Enterprise B2B SaaS companies,' as defined on the company website.) </li>\
              <li>String (Further details on the segment if available, e.g., 'Focuses on medium to large enterprises within the financial services and healthcare sectors.') </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Key Problem(s) It Solves for Users</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (Top critical user pain point or business challenge the product resolves, as highlighted on the company website.) </li>\
              <li>String (Another significant problem it addresses, or details on how it provides a solution.) </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Unique Value Proposition (UVP)</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (The core, compelling reason customers choose this product over alternatives, using language from the company website.) </li>\
              <li>String (The most significant benefit or outcome it distinctively delivers, if stated on the company website.) </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Key Differentiators</h3>\
            <ul class='list-none space-y-1 text-gray-300'>\
              <li>String (A standout aspect - feature, technology, etc. - that sets it apart, as presented on the company website.) </li>\
              <li>String (Another key differentiator, e.g., 'Offers [Unique Aspect A], unlike most competitors who focus on [Common Aspect B].') </li>\
            </ul>\
          </div>"
    },
    {
    "title": "Core Functionality & Value",
    "completed": false,
    "summary": "This module provides a detailed breakdown of the product's essential features, the underlying technology that powers it, how it integrates with other systems, and its revenue generation strategy. This information is critical for understanding the product's operational mechanics and business model.",
    "content": "Explore the intricate mechanics of the product by examining its identified features and their descriptions, revealing what the product does for its users. Understand the key underlying technologies that drive its performance and unique capabilities. Discover how it integrates within a broader ecosystem to enhance value, and analyze its monetization strategy and pricing approach to see how it generates revenue.",
    "htmlContent": "<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Identified Product Features & Descriptions</h3>\
            <ul class='list-none space-y-2 mb-4 text-gray-300'>\
              <li><b>Feature 1: [Feature Name]</b> - String (A 1-2 line summary of what the feature does and its primary user benefit or value, as described on the company website.) </li>\
              <li><b>Feature 2: [Feature Name]</b> - String (Similar detailed description for another feature.) </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Key Underlying Technology</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (Description of specific technology fundamental to its performance or UVP, if detailed on the company website, e.g., 'Leverages proprietary machine learning models for advanced predictive analytics.') </li>\
              <li>String (If standard tech or not detailed, statement like 'Built on a robust and scalable modern tech stack, focusing on reliable delivery of features,' or 'Specific underlying technology details are not highlighted on the website.') </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Integration & Ecosystem Synergy</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (Key integrations critical to user workflows, e.g., with other company products or essential third-party services, as mentioned on the company website.) </li>\
              <li>String (How these integrations extend functionality or streamline user experience, e.g., 'Offers seamless data synchronization with [Contextual Product], enabling a unified workflow for X and Y,' based on website details.) </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Monetization Strategy & Pricing Approach</h3>\
            <ul class='list-none space-y-1 text-gray-300'>\
              <li>String (How the product generates revenue, e.g., 'Tiered subscription model: Basic, Pro, Enterprise,' as stated on the company website.) </li>\
              <li>String (Brief overview of its pricing model or common tiers, e.g., 'Pricing is per user per month, with volume discounts for larger teams,' if available on the website. If not, state that pricing details are not publicly available on the site.) </li>\
            </ul>\
          </div>"
    },
    {
    "title": "User Focus & Core Needs",
    "completed": false,
    "summary": "This module delves into the primary users of the product, describing their profiles, common engagement patterns, and the fundamental needs or aspirations the product helps them achieve. This user-centric view is essential for understanding the product's impact.",
    "content": "Understand the heart of the product's design by exploring its primary target user profiles, detailing who uses it and why. Discover how users typically interact with the product through common workflows, and uncover the fundamental needs and aspirations that the product helps them fulfill, all based on insights from official sources.",
    "htmlContent": "<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Primary Target User Profile(s)</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (Detailed description of the most important user segment or persona, e.g., 'Marketing Managers in mid-sized technology companies requiring advanced campaign analytics,' as defined on the company website.) </li>\
              <li>String (Key characteristics, roles, daily tasks, and motivations of another primary user profile relevant to the product, based on website information.) </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>How Users Engage with the Product</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (Scenario 1: Description of a common workflow or task a user performs with the product, e.g., 'To optimize ad spend, a user first ingests campaign data from multiple sources, then utilizes the platform's attribution modeling feature to identify high-performing channels, and finally generates a comprehensive report for stakeholders.') </li>\
              <li>String (Scenario 2: Similar detailed description for another key interaction or use case, as described or inferred from the company website.) </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Fundamental User Needs Addressed</h3>\
            <ul class='list-none space-y-1 text-gray-300'>\
              <li>String (A core underlying need or 'job' the product helps users accomplish, e.g., 'To gain actionable insights from complex datasets to make data-driven business decisions,' inferred from website information.) </li>\
              <li>String (Another fundamental need or aspiration the product fulfills, framed as the progress users are trying to make, e.g., 'To streamline collaborative project management and improve team productivity on complex initiatives.') </li>\
            </ul>\
          </div>"
    },
    {
    "title": "Competitive Landscape (Product-Focused)",
    "completed": false,
    "summary": "This module examines the competitive environment surrounding the product, identifying both direct and indirect rivals, and detailing the product's strategic positioning and approach to winning in the market. Understanding this landscape is crucial for strategic product development.",
    "content": "Analyze the product's standing within its market by identifying key direct competitors and exploring indirect competition and alternative solutions that address the same user problems. This card details how the product strategically positions itself against these competitors, highlighting its competitive advantages and aspirations for market leadership, drawing on official and general market information.",
    "htmlContent": "<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Key Direct Competitors</h3>\
            <ul class='list-none space-y-2 mb-4 text-gray-300'>\
              <li><b>Competitor A: [Name].</b> String (Known for [Their main strength/focus area]. If competitor details are from general knowledge, state so. If from company website, cite that.) </li>\
              <li><b>Competitor B: [Name].</b> String (Similar detailed description for another direct competitor and its known strengths.) </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Indirect Competition & Alternative Solutions</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (Other ways users currently address the core problem the Primary Focus Product solves, e.g., 'Utilizing generic spreadsheet software for data analysis, which lacks specialized features but is widely accessible,' inferred from product descriptions or general market understanding.) </li>\
              <li>String (Description of another alternative solution or type of indirect competitor, e.g., 'Developing custom in-house tools, which offer tailored functionality but require significant development resources and ongoing maintenance.') </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Positioning Against Competitors</h3>\
            <ul class='list-none space-y-1 text-gray-300'>\
              <li>String (How the product aims to win against direct competitors, e.g., 'By offering a more intuitive user interface and significantly faster data processing speeds, as highlighted by its UVP and differentiators from the company website.') </li>\
              <li>String (Its key competitive advantage in the current landscape, e.g., 'Its unique focus on seamless integration with the broader [Company Name] ecosystem provides a unified user experience not easily matched by standalone competitors.') </li>\
            </ul>\
          </div>"
    },
    {
    "title": "SWOT Analysis",
    "completed": false,
    "summary": "This module provides a strategic SWOT analysis of the product, detailing its internal strengths and weaknesses, along with external opportunities and threats. This comprehensive assessment is vital for understanding the product's current standing and future strategic direction.",
    "content": "Engage in a critical analysis of the product's strategic position through a SWOT framework. Uncover its internal strengths and weaknesses, leveraging insights primarily from company official sources. Simultaneously, explore external opportunities for growth and potential threats that could impact its trajectory, drawing on both official information and broader market knowledge.",
    "htmlContent": "<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Strengths</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (A key internal advantage, e.g., 'Leverages [Company Name]'s strong brand reputation and existing enterprise customer base for market penetration,' derived from website and JD analysis.) </li>\
              <li>String (Another core competency, e.g., 'Possesses proprietary algorithms for [specific function] that deliver demonstrably superior accuracy compared to alternatives, as evidenced by case studies on the company website.') </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Weaknesses</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (An internal limitation, e.g., 'The product currently has a steeper learning curve for non-technical users, potentially hindering wider adoption in certain segments,' inferred cautiously from website or JD.) </li>\
              <li>String (Another area for improvement, e.g., 'Perceived as having a higher price point compared to some newer, more narrowly focused competitors, which could be a barrier for smaller businesses.') </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Opportunities</h3>\
            <ul class='list-none space-y-1 mb-4 text-gray-300'>\
              <li>String (A significant external market opportunity, e.g., 'The rapidly growing market demand for AI-powered automation in [target industry] presents a significant expansion opportunity for the product’s advanced capabilities.') </li>\
              <li>String (Another potential opportunity, e.g., 'The increasing need for robust data privacy and compliance features offers a chance to further differentiate by enhancing its existing security architecture.') </li>\
            </ul>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Threats</h3>\
            <ul class='list-none space-y-1 text-gray-300'>\
              <li>String (A key external threat, e.g., 'Intense competition from both established players and agile startups introducing innovative features at a rapid pace, requiring continuous product development.') </li>\
              <li>String (Another potential challenge, e.g., 'Potential shifts in technology standards or user preferences towards open-source alternatives could impact long-term market share if not proactively addressed.') </li>\
            </ul>\
          </div>"
    }
    ],
    "questions":"You are an expert product analyst and interviewer. Your task is to generate a set of relevant and insightful product research questions for a thorough analysis of [product_name]. **IMPORTANT:** Do not generate any answers; provide only the questions. Please generate 5-7 distinct questions that cover the following areas of product research: * **Problem and User Value:** Questions about the core problem the product solves, its target users, and the value it delivers. * **Competitive Landscape:** Questions focused on how the product stands out from competitors. * **Feature Analysis & Prioritization:** Questions about existing features, their effectiveness, and potential future improvements. * **Risks and Challenges:** Questions that explore potential obstacles to the product's success. Ensure the questions are open-ended and designed to elicit detailed, analytical responses from a product expert. --- **Replace `[product_name]` with the actual name of the product you want to analyze** (e.g., \"Google Maps\", \"Slack\", \"Netflix\", \"ChatGPT\")."
    }
    ''')
    return product_research

def job_description_analysis_fun(data):
    job_description_analysis = (f'''Analyse this entire {data}'''
                                 
                                '''
    ----
    # Job Description Analysis —> Decode The Role (JD Analysis)

**Updated Plain Text Breakdown (Module 3: Decode the Role - 4 Cards):**

**Module Title:** Decode the Role

Quick Summary Instructions:

    Generate a concise (3-4 sentence) overview.

    Explicitly state that this analysis is based only on the provided JD text.

    Synthesize the role's core purpose, the most critical skill/experience emphasized, the primary way success appears to be measured, and the main organizational context (reporting line or key collaborators).

---

Card 1: Core Role & Responsibilities

    Title: Core Role & Responsibilities

    Summary: Analysis of the main purpose of the role and key tasks specified in the JD, interpreted for their significance.

    htmlContent:

        - Wrap the entire content in a `<div>` with proper padding and spacing.
- Use modern UI practices inspired by Clerk UI: soft shadows, rounded corners, spacing between sections, clean typography, and logical layout grouping.
- Use Tailwind utility classes only for layout, text, cards, dividers, tables, etc.
- Include:
  - Headings for each main point (e.g., “Primary Mission / Underlying Need”)
  - Sub-points as bullet lists or brief paragraphs depending on their content
  - Tables if grouping helps clarity
  - Dividers (`<hr>`) between sections
- Ensure good use of whitespace and spacing to avoid clutter
- All points must be converted into attractive, modern, readable HTML
- Do not add any asterisk symbols anywhere
- Begin the HTML directly with a `<div>` tag (do not include `<html>`, `<head>`, etc.)
- Do not include title "Core Role & Responsibilities" and description just start with points
- Include proper spacing classes between list,etc.


Card 2: Required Skills & Experience

    Title: Required Skills & Experience

    Summary: Interpretation of the essential and preferred qualifications sought, explaining their relevance to the role's demands.

    htmlContent:
    - Begin directly with a `<div>` tag (do not include `<html>`, `<head>`, etc.)
- Wrap the entire content in a properly padded and spaced `<div>`
- Use a card-style layout with rounded corners, subtle shadows, and good spacing
- Use headings for the card title and section titles (e.g., “Essential Hard Skills / Technical Requirements”)
- Use readable font sizes, consistent spacing, and neutral color palette like Clerk UI
- Use bullet points or paragraphs for sub-points
- Use dividers (`<hr>`) between each main section
- Include explanation text for each sub-point where applicable
- Do not add any asterisk symbol anywhere in the entire HTML
- Do not include title "Required Skills & Experience" and description just start with points
- Include proper spacing classes between list,etc.


Card 3: Defining Success & Measuring Impact

    Title: Defining Success & Measuring Impact

    Summary: Analysis of how performance will be measured and the expected tangible outcomes of the role, based on explicit and inferred JD points.

    htmlContent:

        - Begin the content directly with a <div> (no <html>, <head>, etc.)
- Wrap the card in a max-width container with padding, rounded corners, and soft shadows
- Use section headers (e.g., “Explicitly Stated Success Metrics / KPIs”) as bold, readable titles
- Render summary as a short paragraph below the card title
- Format sub-points as bullet lists or concise paragraphs, styled with good spacing and readability
- Insert horizontal dividers (`<hr>`) between sections
- Maintain a minimal, neutral color scheme with Tailwind classes for text, background, spacing, and layout
- Use whitespace, padding, and font-weight to create a clear hierarchy
- Do not add any asterisk symbols anywhere
- Do not include title "Defining Success & Measuring Impact" and description just start with points
- Include proper spacing classes between list,etc.


Card 4: Team, Collaboration & Reporting Structure

    Title: Team, Collaboration & Reporting Structure

    Summary: Analysis of the organizational context, including reporting lines, key partners, and the expected style and challenges of collaboration.

    htmlContent:
    - Start directly with a <div> tag (do not include <html>, <head>, etc.)
- Wrap everything inside a container with padding, rounded corners, and soft shadows
- Use well-structured headings for card title and section titles
- Display the summary as a short paragraph under the card title
- Present sub-points as clearly formatted text or bullet points
- Insert <hr> elements between main sections for separation
- Use neutral, readable typography with good spacing and layout
- Follow a professional style similar to Clerk UI (spaced layout, minimalist design, soft shadows)
- Avoid any use of asterisk symbols
- Do not include title "Team, Collaboration & Reporting Structure" and description just start with points
- Include proper spacing classes between list,etc.


Card 5: Strategic Context & Role Significance

    Title: Strategic Context & Role Significance

    Summary: Places the role within the broader company and product strategy, interpreting why this position is important now and its potential impact.

    htmlContent:

        - Begin the HTML directly with a <div> tag (no <html>, <head>, etc.)
- Use a card-style container with padding, rounded corners, shadows, and max width
- The title should be prominent with large, bold font
- Display the summary (if any) or introductory sentence using muted text under the title
- For each main point:
  - Use a clear subheading (e.g., “The Company's Need for this Role”)
  - Present sub-points as paragraphs or bullet points with soft text color
- Use <hr> to separate main points
- Follow professional UI/UX principles like good whitespace, text hierarchy, and spacing
- Make everything visually clean, responsive, and styled like Clerk UI
- Do not include any asterisk symbols anywhere in the HTML
- Do not include title "Strategic Context & Role Significance" and description just start with points
- Include proper spacing classes between list,etc.


Card 6: Key Themes & Interview Angles

    Title: Key Themes & Interview Angles

    Summary: Synthesizes overarching themes from the JD and suggests areas to focus on during interview preparation and discussion.

    htmlContent:
    - Start the content directly with a <div> (no <html> or <head>)
- Use a card-style layout with appropriate padding, spacing, and rounded corners
- Include a bold, clear card title and a paragraph summary at the top
- For each main point:
  - Use a subheading with distinct font size and color
  - Display sub-points as readable paragraphs or lists
- Insert horizontal <hr> elements to visually separate each main section
- Maintain a soft color palette, readable font, good whitespace, and balanced spacing — like Clerk UI
- The layout should be fully responsive and clean without visual clutter
- Do not use any asterisk symbol anywhere
- Do not include title "Key Themes & Interview Angles" and description just start with points
- Include proper spacing classes between list,etc.

----
in each sub module the completed must be false only

---
    ----
    Give me response in this JSON format only and `do not add any asterisk symbol in subPoints`:
    {
    "quick_summary": "Very long information description that summarizes all of these cards or sub modules",
    "sub_modules": [
        {
        "title": "Core Role & Responsibilities",
"completed":false,
        "summary": "This module dissects the job description to pinpoint the fundamental purpose of the role, the primary responsibilities, and the specific activities a successful candidate will undertake. It provides a foundational understanding of the day-to-day expectations and strategic impact of the position.",
        "content": "Gain a deep understanding of the role's core mission and the underlying need it addresses within the organization. This section outlines the key responsibility areas, highlighting the specific product management activities, and identifies areas of particular emphasis or complexity as indicated in the job description.",
        "htmlContent":"<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Primary Mission / Underlying Need</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Key Responsibility Areas & PM Activities</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Areas of Specific Emphasis or Complexity</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>some main title</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>some main title</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>some main title</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
          </div>"
        },
        {
        "title": "Required Skills & Experience",
"completed":false,
        "summary": "This module deciphers the essential and preferred qualifications from the job description, providing a clear understanding of the technical, soft, and experiential skills required for success. It clarifies the relevance of each requirement to the demands of the role.",
        "content": "Explore the critical blend of essential hard skills and technical requirements necessary for this role, alongside the crucial soft skills and attributes that enable effective collaboration and leadership. This section also outlines the required experience level and specific domain knowledge, concluding with an overview of preferred or standout qualifications that can set a candidate apart.",
        "htmlContent":"<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Essential Hard Skills / Technical Requirements</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Critical Soft Skills & Attributes</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Required Experience Level & Domain</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Preferred / Standout Qualifications</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
          </div>"
        },
        {
        "title": "Defining Success & Measuring Impact",
"completed":false,
        "summary": "This module analyzes how success in the role is defined, detailing both explicit metrics and implied indicators of performance. It also explains the expected business and product impact, providing a clear picture of how contributions will be measured and valued within the organization.",
        "content": "Understand the key performance indicators and explicitly stated success metrics that will define achievement in this role. Discover the implied success indicators and the expected business or product impact derived from the job description. This section also offers guidance on how to connect your past achievements to these success criteria for interview examples.",
        "htmlContent":"<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Explicitly Stated Success Metrics / KPIs</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Implied Success Indicators</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Expected Business / Product Impact</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Connecting Success to Interview Examples</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
          </div>"
        },
        {
        "title": "Team, Collaboration & Reporting Structure",
"completed":false,
        "summary": "This module offers an in-depth look at the role's organizational context, including its reporting lines, key internal and external collaborators, and the anticipated collaboration style. It also highlights potential challenges to effective teamwork, providing a holistic view of the social and structural dynamics of the position.",
        "content": "Understand where this role fits within the organizational hierarchy by examining its reporting structure. Identify key internal collaborators and stakeholders you'll work closely with, as well as crucial external relationships. This section also sheds light on the implied collaboration style and potential challenges, preparing you for the interpersonal dynamics of the role.",
        "htmlContent":"<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Reporting Structure</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Key Internal Collaborators / Stakeholders</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Key External Collaborators / Relationships</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Implied Collaboration Style & Potential Challenges</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
          </div>"
        },
        {
        "title": "Strategic Context & Role Significance",
"completed":false,
        "summary": "This module positions the role within the broader strategic landscape of the company and its product portfolio. It clarifies the organization's current need for this specific role, how it contributes to overarching company and product strategies, and the potential impact a successful candidate can have.",
        "content": "Discover the strategic importance of this role by understanding the company's current need and how this position contributes to the broader product and company strategy. Explore potential strategic challenges or opportunities the role might face, and assess the level of autonomy and influence you can expect to have within the organization.",
        "htmlContent":"<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>The Company's Need for this Role</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Contribution to Broader Product / Company Strategy</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Potential Strategic Challenges or Opportunities</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Role Autonomy and Influence Level</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
          </div>"
        },
          {
        "title": "Key Themes & Interview Angles",
"completed":false,
        "summary": "This module distills the job description into overarching themes and suggests specific angles for interview preparation. It highlights areas likely to be deeply probed during interviews and provides guidance on how to effectively align your experience and formulate insightful questions to ask the interviewer.",
        "content": "Identify the overarching themes and priorities embedded within the job description, guiding your overall interview strategy. This section pinpoints areas likely to be deeply probed by interviewers and offers actionable advice on how to effectively align your experience with the role's requirements. Finally, it suggests insightful questions to ask, demonstrating your engagement and understanding.",
        "htmlContent":"<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Overarching Themes & Priorities</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Areas Likely to be Deeply Probed</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>How to Align Your Experience</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Insightful Questions to Ask</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
          </div>"
        }
    ]
    }

    ''')
    return job_description_analysis

def resume_experience_to_highlight_to_stand_out_fun(data):
    resume_experience_to_highlight_to_stand_out = (f'''Analyse this entire {data}'''

    '''
----
# Resume Experience You Can Highlight to Stand Out — Module 4

**Updated Plain Text Breakdown (Module 4: Resume Alignment & Differentiators - 3 Cards):**

**Module Title:** Resume Experience You Can Highlight to Stand Out

Quick Summary Instructions:

    Generate a concise (3–4 sentence) overview.
    Clearly state this is based on the comparison between Resume and JD.
    Synthesize where the candidate is strongest, where alignment is partial or missing, and which achievements should be emphasized to differentiate.

---

Card 1: Key Strengths & Alignment

    Title: Key Strengths & Alignment

    Summary: Pinpoints where the resume aligns directly with the JD, surfacing the most relevant strengths and how they map to the job expectations.

    htmlContent:
    - Begin directly with a `<div>` tag (no `<html>`, `<head>`, etc.)
- Wrap everything in a padded, clean container with rounded corners and modern layout
- Use readable fonts and logical structure with good spacing
- Use Tailwind classes for layout, spacing, text, and visual grouping
- Use headings for each major theme (e.g., “Highly Relevant Technical Skills”)
- Present sub-points as bullet lists or short paragraphs
- Use `<hr>` between key groupings
- Do not include the card title or summary in the HTML output
- Do not use any asterisk symbol anywhere
- Include proper spacing classes between list, sections, etc.

---

Card 2: Potential Gaps & How to Address

    Title: Potential Gaps & How to Address

    Summary: Identifies where the resume may fall short of JD expectations, and gives framing strategies to bridge these during interviews.

    htmlContent:
    - Start directly with a `<div>` tag (no `<html>`, `<head>`, etc.)
- Use soft, professional visual styling: padding, shadows, neutral color palette, readable text
- Headings for each type of gap or concern
- Under each heading, list action-oriented advice or framing strategies as bullets or paragraphs
- Ensure spacing between sections using Tailwind classes
- Use `<hr>` between each main section
- Do not include title or description in the HTML output
- Do not use any asterisk symbols
- Maintain modern layout structure (Clerk UI–like)

---

Card 3: Standout Experiences to Highlight

    Title: Standout Experiences to Highlight

    Summary: Identifies 2–4 specific accomplishments from your resume that are particularly impactful for this role, with guidance on how to frame them during interviews.

    htmlContent:
    - Begin directly with a `<div>` tag (no `<html>`, `<head>`, etc.)
- Wrap in a card-style layout with padding, rounded corners, good spacing
- Use bold subheadings for each experience or grouping
- Under each, list supporting points, explanations, or talking points
- Use Tailwind utility classes for structure and readability
- Insert `<hr>` tags between major sections
- Avoid visual clutter and maintain whitespace
- Do not include card title or summary in HTML
- No asterisk symbols anywhere
- Include proper spacing between sections

----

In each sub module the completed must be false only

----
Give me response in this JSON format only and `do not add any asterisk symbol in subPoints`:
{
"quick_summary": "Very long information description that summarizes all of these cards or sub modules",
"sub_modules": [
    {
    "title": "Key Strengths & Alignment",
    "completed": false,
    "summary": "This module pinpoints the direct alignments between your resume and the job description, highlighting your most relevant strengths. It showcases how your experience, skills, and knowledge directly map to the role's expectations, providing a solid foundation for your candidacy.",
    "content": "Identify highly relevant technical skills that match the JD, showcase your business and domain knowledge fit, and detail experience that aligns perfectly with the scope of the role. Emphasize your readiness for team collaboration, highlight communication or leadership strengths, and reveal any unique background or edge that makes you stand out.",
    "htmlContent":"<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Highly Relevant Technical Skills</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Business/Domain Knowledge Fit</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Experience That Matches Scope</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Team/Collaboration Readiness</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Communication or Leadership Strengths</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Unique Background or Edge</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
          </div>"
    },
    {
    "title": "Potential Gaps & How to Address",
    "completed": false,
    "summary": "This module identifies potential areas where your resume might not fully meet the job description's expectations. It also provides strategic advice and framing techniques to effectively address these gaps during interviews, turning potential weaknesses into opportunities for discussion.",
    "content": "Recognize missing specific tool or technology experience, address shorter durations in similar roles, and acknowledge limited exposure to certain business models. Crucially, learn effective ways to frame your transferable skills and experiences to bridge any perceived gaps during your interview.",
    "htmlContent":"<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Missing Specific Tool/Technology Experience</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Shorter Duration in Similar Roles</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Limited Exposure to Certain Business Models</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Ways to Frame Transferable Skills</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
          </div>"
    },
    {
    "title": "Standout Experiences to Highlight",
    "completed": false,
    "summary": "This module identifies your most impactful accomplishments from your resume that resonate strongly with the job's requirements. It provides guidance on how to effectively frame these experiences during interviews, ensuring they demonstrate your unique value and differentiate you from other candidates.",
    "content": "Pinpoint specific projects or initiatives that showcase your capabilities, such as Project/Initiative 1 and Project/Initiative 2, detailing their context and your contributions. Additionally, identify impactful experience 3 that demonstrates your unique value, and articulate your unique contribution or edge that sets you apart from other candidates.",
    "htmlContent":"<div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Project/Initiative 1 (Title/Context)</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Project/Initiative 2 (Title/Context)</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Impactful Experience 3 (Title/Context)</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
            <hr class='my-4 border-gray-700'>\
            <h3 class='text-lg font-semibold mb-2 text-gray-50'>Unique Contribution or Edge</h3>\
            <p class='text-gray-300 mb-2'>information description 1</p>\
            <p class='text-gray-300'>information description 2</p>\
          </div>"
    }
]
}
    ''')
    return resume_experience_to_highlight_to_stand_out

def recruiter_screen_preparation_fun(data):
    recruiter_screen_preparation = (f'''Analyse this entire {data}'''

'''
----
Act as an expert career coach specializing in early-stage interview 
preparation. Analyze the provided Job Description (JD) and typical 
recruiter screen objectives to generate a comprehensive guide for the
candidate's first call with a recruiter.

This guide includes 4 modules designed to ensure the candidate is 
well-prepared, confident, and aligned with the expectations set forth 
by the JD. The insights are tailored using the JD as the primary source 
of truth and only use the Resume (if available) for crafting the introduction pitch.

----
Give me response in this JSON format only and do not include asterisk symbols in subPoints:

{
"quick_summary": "This module equips candidates with a recruiter-specific prep strategy based on the JD provided. It outlines expected recruiter screening goals, provides quick facts, helps shape a tailored self-introduction, anticipates common recruiter questions, and suggests thoughtful questions the candidate should ask. All content is structured to boost candidate clarity, confidence, and conversational readiness in early-stage calls.",
"sub_modules": [
    {
    "title": "Call Rubric & Quick Facts",
    "completed": false,
    "summary": "This card describes the purpose and structure of the recruiter screen, offering a clear view of how the candidate will be evaluated. It summarizes what recruiters typically look for, and extracts JD-specific logistics like salary and location when available.",
    "content": "A comprehensive breakdown of call goals, key fit checks, and recruiter-facing evaluation themes.",
    "htmlContent":"\
    <div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
        <h2 class='text-xl font-semibold text-gray-50'>Purpose of the Recruiter Screen</h2>\
        <p class='text-gray-300'>To assess a candidate's overall fit for the role based on their qualifications, communication skills, enthusiasm for the position, and logistical alignment with job requirements. This initial call helps recruiters determine if the candidate should move forward in the interview process.</p>\
        <hr class='my-4 border-gray-700'>\
        \
        <h2 class='text-xl font-semibold text-gray-50'>Key Evaluation Areas</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>Relevance of Experience:</span> Does the candidate's professional background align with the core responsibilities and requirements outlined in the JD?</li>\
            <li><span class='font-medium'>Communication Skills:</span> Can the candidate articulate their experiences and thoughts clearly and concisely?</li>\
            <li><span class='font-medium'>Interest and Enthusiasm:</span> Is the candidate genuinely interested in this specific role and the company, demonstrating that they have researched both?</li>\
            <li><span class='font-medium'>Logistical Alignment:</span> Are salary expectations, location preferences, and availability in line with what the role offers?</li>\
        </ul>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Salary Information from JD</h2>\
        <p class='text-gray-300'>Salary information was not explicitly provided in the Job Description. Candidates should be prepared to discuss their salary expectations based on market research for similar roles.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Location & Remote Status from JD</h2>\
        <p class='text-gray-300'>The Job Description did not clearly specify the exact location or remote work status for this role. It's important to clarify this with the recruiter during the call.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Other Logistical Details</h2>\
        <p class='text-gray-300'>No specific logistical or compliance constraints, such as required travel percentage, specific work hours, or security clearances, were mentioned in the Job Description. Candidates should be prepared to address any standard logistical questions.</p>\
    </div>"
    }},
    {
    "title": "Craft Your Introduction",
    "completed": false,
    "summary": "This card provides a structured yet flexible framework for the candidate to deliver a concise and compelling self-introduction. It guides them in connecting their past experiences and present skills with the expectations outlined in the Job Description, ensuring their pitch resonates with the recruiter’s objectives.",
    "content": "This card empowers the candidate to deliver a confident 'Tell me about yourself' answer using the Past-Present-Future model, ensuring it's tailored to the specific role and company, making an immediate positive impression.",
    "htmlContent":"\
    <div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
        <h2 class='text-xl font-semibold text-gray-50'>Strategy for Tailoring Your Pitch</h2>\
        <p class='text-gray-300'>Employ the <span class='font-medium'>Past-Present-Future</span> framework to structure your introduction, ensuring it’s concise, relevant, and compelling. Start with your journey, explain your current role and key contributions, and conclude by connecting your aspirations to this specific opportunity. Integrate themes, skills, and values emphasized in the Job Description.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Key Elements to Highlight (Based on JD & Resume)</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>Relevant Experience:</span> Showcase projects or roles where you managed responsibilities directly aligned with the job’s scope (e.g., product launch, feature development, market analysis).</li>\
            <li><span class='font-medium'>Specific Skills and Tools:</span> Highlight any technical skills, software proficiency, or methodologies explicitly mentioned in the JD (e.g., agile methodologies, data analytics tools, specific programming languages).</li>\
            <li><span class='font-medium'>Impactful Outcomes:</span> Quantify your achievements where possible (e.g., 'increased user engagement by X%', 'reduced operational costs by Y%').</li>\
            <li><span class='font-medium'>Collaboration and Leadership:</span> If the JD emphasizes teamwork, cross-functional collaboration, or leadership, provide examples that demonstrate these capabilities.</li>\
        </ul>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Connecting Your Experience to the Role</h2>\
        <p class='text-gray-300'>Actively use keywords and phrases from the Job Description when describing your past experiences. For instance, if the JD emphasizes 'cross-functional collaboration,' explicitly state how you've 'successfully collaborated cross-functionally' in previous roles. This demonstrates direct alignment and attention to detail.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Practice and Timing</h2>\
        <p class='text-gray-300'>Keep your introduction to an ideal length of <span class='font-medium'>2-3 minutes</span>. Rehearse it multiple times to ensure clarity, conciseness, and a confident, natural delivery. Practice in front of a mirror or record yourself to refine your pacing and tone.</p>\
    </div>"
    }},
    {
    "title": "Insightful Questions to Ask",
    "completed": false,
    "summary": "This card offers a curated list of insightful questions for the candidate to ask the recruiter. These questions are designed to demonstrate genuine interest, strategic thinking, and a proactive approach, while also helping the candidate gather crucial information about the role, team, and company culture.",
    "content": "This module prepares the candidate with a set of smart, strategic questions to ask the recruiter, categorized for ease of access and designed to elicit valuable information while showcasing the candidate's preparation and critical thinking.",
    "htmlContent":"\
    <div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
        <h2 class='text-xl font-semibold text-gray-50'>Questions About the Role & Team</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>Immediate Priorities:</span> 'What would be the top 2-3 immediate priorities for someone stepping into this role in the first 3-6 months?' This helps understand initial focus and expectations.</li>\
            <li><span class='font-medium'>Team Dynamics:</span> 'Could you tell me a bit more about the team this role sits within? How large is it, and what are its key functions?' This provides context on collaboration and structure.</li>\
            <li><span class='font-medium'>Success Measurement:</span> 'How is success typically measured for someone in this position within the first year?' This clarifies performance benchmarks.</li>\
            <li><span class='font-medium'>Growth Opportunities:</span> 'What are the potential career growth or development opportunities associated with this role?' This indicates long-term potential.</li>\
        </ul>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Questions About the Interview Process</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>Next Steps:</span> 'What does the remainder of the interview process look like, and what can I expect in terms of timelines?' This sets expectations for the candidate.</li>\
            <li><span class='font-medium'>Role Fill Timeline:</span> 'Are you looking to fill this role by a specific date, or is the timeline more flexible?' This provides insight into urgency.</li>\
            <li><span class='font-medium'>Key Stakeholders:</span> 'Who are the key individuals I would be meeting in subsequent rounds, and what are their roles?' This helps the candidate prepare for future interviews.</li>\
        </ul>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Questions About Culture and Team Environment</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>Company Culture:</span> 'How would you describe the overall culture at [Company Name], particularly within the team for this role?' This helps assess cultural fit.</li>\
            <li><span class='font-medium'>Success Traits:</span> 'In your experience, what are some common traits or qualities you've observed in individuals who thrive in this company/team environment?' This offers insights into desired characteristics.</li>\
        </ul>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Clarifying JD Details</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>Specific Responsibility Clarification:</span> 'In the Job Description, it mentions 'strategic impact on product roadmap.' Could you elaborate on what that typically entails for this role?' This demonstrates attention to detail in the JD.</li>\
            <li><span class='font-medium'>Technology/Tool Usage:</span> 'The JD lists [specific technology/tool]. Can you describe how frequently this tool is used, or its significance to daily tasks?' This helps understand practical application.</li>\
        </ul>\
    </div>"
    }}
]
}
''')
    return recruiter_screen_preparation

def favorite_product_question_fun(data):
    favorite_product_question = (f'''Analyse this entire {data}'''

'''
----
This module helps you confidently answer one of the most common product management interview questions — “What’s your favorite product and how would you improve it?” It breaks down interviewer intent, question types, and gives a powerful 5-step framework to structure your response with depth and clarity.

----
Give me response in this JSON format only and do not include any asterisk symbols in htmlContent:

{
"quick_summary": "This guide offers structured preparation to tackle the popular 'Favorite Product' interview question. It explains the reasoning behind the question, what follow-ups to expect, how to select a meaningful product, and how to suggest intelligent improvements. The second card introduces a 5-step framework to organize your answer clearly, show empathy for users, and demonstrate product thinking in action.",
"sub_modules": [
    {
    "title": "What’s Your Favorite Product?",
    "completed": false,
    "summary": "This section delves into the 'Favorite Product' interview question, explaining the interviewer's motivations and various question formats. It offers practical advice on selecting a compelling product and framing insightful improvements, ensuring a well-rounded and impactful response.",
    "content": "This module helps demystify a common interview favorite, offering techniques to build a high-impact response grounded in personal insight and structured thinking.",
    "htmlContent":"\
    <div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
        <h2 class='text-xl font-semibold text-gray-50'>Why Do Interviewers Ask This?</h2>\
        <p class='text-gray-300'>Interviewers use this question as a low-pressure entry point to assess several key product management skills. They want to evaluate your product thinking abilities, your capacity for user empathy, and the clarity of your communication. It also provides insight into how you analyze product tradeoffs and the types of products you personally engage with and appreciate.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>What to Expect</h2>\
        <p class='text-gray-300'>This question is typically asked early in product management interviews, often as an icebreaker. Expect it to lead into a 5–10 minute casual conversation. Common follow-up questions include 'How would you improve it?' or 'How would you measure the success of your proposed improvements?'</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Common Variants</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>Company-Specific:</span> 'What’s your favorite Google product (or a product from our competitor)?'</li>\
            <li><span class='font-medium'>Negative Framing:</span> 'What’s a product you hate that others love, and why?'</li>\
            <li><span class='font-medium'>Future-Oriented:</span> 'What’s a product with untapped potential, and how would you unlock it?'</li>\
            <li><span class='font-medium'>Alternative:</span> 'Tell me about a product that has profoundly impacted your daily life.'</li>\
        </ul>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>How to Choose a Good Product</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>Genuine Interest:</span> Pick something you genuinely care about and have formed strong opinions on. Your passion will shine through.</li>\
            <li><span class='font-medium'>Complexity & Nuance:</span> Choose products that have meaningful pros and cons, allowing you to discuss trade-offs and design decisions.</li>\
            <li><span class='font-medium'>Avoid Direct Competitors:</span> Steer clear of products that are direct competitors of the interviewing company, unless you can offer a highly diplomatic and constructive critique.</li>\
            <li><span class='font-medium'>Depth over Simplicity:</span> Avoid overly simple or trivial products that don't allow for in-depth product analysis or improvement suggestions.</li>\
        </ul>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Example Product Improvement</h2>\
        <p class='text-gray-300'>“One specific area I’d focus on for Notion is enhancing its search experience. While functional, it could be greatly improved by introducing a lightweight, intelligent tagging system. This system would dynamically group and surface related content based on tags, making it significantly easier for users to synthesize information and quickly find what they need across their vast workspaces.”</p>\
    </div>"
    },
    {
    "title": "5 Steps Framework",
    "completed": false,
    "summary": "This section presents a robust 5-step framework for structuring your 'Favorite Product' answer. It guides you from selecting the right product to defining its users, identifying pain points, and proposing thoughtful improvements, all while demonstrating product empathy and user-centric thinking.",
    "content": "This framework ensures your response includes product empathy, user-centric thinking, and actionable improvement ideas, making your answer comprehensive and impressive.",
    "htmlContent":"\
    <div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
        <h2 class='text-xl font-semibold text-gray-50'>1. Pick the Right Product</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>Prepare a Portfolio:</span> Have 3-4 products ready, ideally a mix of digital (e.g., app, software, website) and at least 1 physical product. This shows versatility.</li>\
            <li><span class='font-medium'>Strategic Choices:</span> Avoid products that are either culturally niche (unless you have a compelling, widely understandable reason) or overly common (like Google Search) unless you have a truly unique, insightful take on them.</li>\
        </ul>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>2. Introduce the Product in One Sentence</h2>\
        <p class='text-gray-300'>Start with a crisp, clear, and concise description that immediately tells the interviewer what the product does. For example: <span class='font-medium'>“My favorite product is Waze, a navigation app that helps users get to their destination efficiently by leveraging real-time crowd-sourced traffic data.”</span></p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>3. Define Customer Segments & Your Relation</h2>\
        <p class='text-gray-300'>Identify 2-4 key user segments for the product. Then, share which segment you personally relate to the most and why. This demonstrates user empathy and personal connection. Example: <span class='font-medium'>“Waze serves daily commuters, long-distance travelers, and professional drivers. As a new parent, I particularly value Waze because it helps me avoid unpredictable traffic, ensuring smoother and less stressful drives with my baby.”</span></p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>4. Explain Pain-Driven Features</h2>\
        <p class='text-gray-300'>Describe how the product addresses specific user pain points through its features. Use a clear structure: <span class='font-medium'>Pain → Feature → Outcome.</span> Provide 1-2 examples. Example: <span class='font-medium'>“The pain point is the stress and unpredictability of getting stuck in traffic with kids in the car. Waze’s key feature is its real-time rerouting based on live user reports and traffic conditions. The outcome for me is that I can stay calm, avoid significant delays, and reach my destination faster and more reliably.”</span></p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>5. Suggest Improvements & Justify</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>Mission Alignment:</span> Ensure your proposed improvement aligns with the company's overall mission and the product's core value proposition.</li>\
            <li><span class='font-medium'>Address Unmet Needs:</span> Focus on an unmet user need or an existing pain point that isn't fully resolved.</li>\
            <li><span class='font-medium'>Leverage Technology:</span> Consider how new technologies or existing capabilities could enhance the product.</li>\
            <li><span class='font-medium'>Enhance User Journey:</span> Think about improving the end-to-end user experience, perhaps through better integration with other services (e.g., media streaming, calendar syncing).</li>\
            <li><span class='font-medium'>Prioritization & Trade-offs:</span> Briefly mention how you'd prioritize this improvement and any potential trade-offs (e.g., engineering effort, impact on other features).</li>\
        </ul>\
    </div>"
    }}
]
}
'''
)
    return favorite_product_question

def product_design_fun(data):
    product_design = (f'''Analyse this entire {data}'''

'''
----
This module helps candidates master product design interview questions. It includes an overview of what to expect, how to think through structured responses, and practice with example questions aligned to a company's domain or industry.

----
Give me response in this JSON format only and ensure do not use any asterisk symbols anywhere:

{
"quick_summary": "This comprehensive module prepares you for product design interview questions. It breaks down how to approach these questions, what interviewers evaluate, and how to elevate your response from good to great. You’ll learn a step-by-step framework including clarifying the prompt, identifying users, understanding their pain points, brainstorming solutions, and defining success metrics. It also provides company-specific sample questions to help you simulate real interviews.",
"sub_modules": [
    {
    "title": "Overview of Product Design Questions",
    "completed": false,
    "summary": "This card provides a foundational understanding of product design interviews. It covers expectations, what interviewers assess, sample responses, and a rubric to distinguish between performance levels.",
    "content": "Get familiar with how product design questions work, why they’re asked, and how to recognize the difference between an average and an outstanding answer.",
    "htmlContent": "\
    <div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
        <h2 class='text-xl font-semibold text-gray-50'>What to Expect</h2>\
        <p class='text-gray-300'>Product design interview questions are typically open-ended and challenge your problem-solving abilities. You can expect prompts such as “Design X for Y” or “Improve Z.” Your responses will be evaluated on your ability to structure your thoughts, demonstrate creativity, and show genuine user empathy. A typical response flow involves: Clarifying the problem -> Defining Users -> Identifying Pain Points -> Brainstorming Solutions -> Defining Success Metrics.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>What Interviewers are Looking For</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>Product Sense and Structured Thinking:</span> Your ability to break down complex problems into manageable parts and approach them logically.</li>\
            <li><span class='font-medium'>User Empathy and Prioritization:</span> Understanding user needs deeply and prioritizing which problems to solve first based on impact and feasibility.</li>\
            <li><span class='font-medium'>Creativity Balanced with Feasibility:</span> Generating innovative ideas while considering technical, business, and operational constraints.</li>\
            <li><span class='font-medium'>Strong Communication and Decision Rationale:</span> Clearly articulating your thought process, assumptions, and the reasoning behind your choices.</li>\
        </ul>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Sample Answers: Good vs. Great</h2>\
        <p class='text-gray-300'>A <span class='font-medium'>“Good”</span> answer will typically follow a basic framework, outlining users and solutions, but may lack depth in insight or justification for prioritization. It might address the prompt but without significant innovation or deep user understanding. A <span class='font-medium'>“Great”</span> answer, however, uses a robust framework, thoroughly prioritizes pain points with clear rationale, explains trade-offs thoughtfully, and demonstrates a profound understanding of user needs, business goals, and technical considerations. It also includes clear success metrics.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Why do companies ask Product Design questions</h2>\
        <p class='text-gray-300'>These questions are designed to simulate real-world product challenges and assess how you perform under pressure. They reveal your capacity to define problems, empathize with different user segments, ideate creative and practical solutions, and consider the feasibility and measurable success of your proposals. It helps interviewers understand your end-to-end product thinking process.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Evaluation Rubric</h2>\
        <p class='text-gray-300'>Interviewers typically evaluate your answer across several dimensions: your ability to frame the problem, the logical structure of your response, the creativity of your solutions, the clarity of your communication, and how well your proposed solutions align with user needs and business objectives. Performance levels might range from <span class='font-medium'>Poor</span> (disorganized, lacks user focus), to <span class='font-medium'>Good</span> (structured but generic), to <span class='font-medium'>Great</span> (insightful, well-prioritized, practical, and clearly communicated with strong rationale).</p>\
    </div>"
    },
    {
    "title": "How to Answer Product Design Questions",
    "completed": false,
    "summary": "This card details a comprehensive, step-by-step framework for answering product design questions. It guides you from clarifying the initial prompt to defining success metrics, ensuring your responses are user-centered, well-reasoned, and clearly articulated.",
    "content": "Learn the full structure to solve product design questions, starting with clarifying the context and ending with success metrics.",
    "htmlContent": "\
    <div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
        <h2 class='text-xl font-semibold text-gray-50'>1. Clarify and Get Context</h2>\
        <p class='text-gray-300'>Before diving into solutions, ask clarifying questions to ensure you and the interviewer are on the same page. Key questions include: 'Who are we solving for specifically?', 'What is the primary goal of this design challenge?', 'Are there any specific constraints (e.g., budget, time, technology)?', 'Is this intended for a mobile app, web platform, or another medium?' Clarifying upfront helps align your solution with the interviewer's expectations and demonstrates thoughtful problem-solving.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>2. Mission/Vision Alignment</h2>\
        <p class='text-gray-300'>If the question pertains to a known company, tie your proposed solution back to its overarching mission and vision. This shows you understand the company's strategic direction. If it's a hypothetical scenario or an unknown company, state your assumptions about its mission clearly. For example, 'I will assume the mission is to connect people through shared experiences.' This establishes a guiding principle for your design.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>3. Define Personas (User Groups)</h2>\
        <p class='text-gray-300'>Identify 2-4 distinct user types who would interact with your product. For each persona, consider their goals, motivations, behaviors, and pain points. Prioritize these personas based on factors like their need intensity, frequency of use, or alignment with overall business goals. For example: 'For a trail-finding app, our primary personas might be: avid hikers seeking challenging routes, casual walkers looking for scenic strolls, and tourists interested in local landmarks.'</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>4. User Journey</h2>\
        <p class='text-gray-300'>Map out the typical user's flow through the product, from their initial interaction to achieving their goal. This helps identify key touchpoints and potential areas of friction. For example, for an e-commerce platform, the user journey might be: Search -> Filter -> View Product Details -> Add to Cart -> Checkout -> Receive Order -> Review Product.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>5. Identify User Pain Points and Opportunities</h2>\
        <p class='text-gray-300'>Based on your user journey, pinpoint specific points of friction, unmet needs, or frustrations that users might experience. These are your pain points, which represent opportunities for improvement or new features. Focus on the high-impact problems that, if solved, would significantly improve the user experience or align with business objectives. For instance, 'Users struggle with inaccurate filters leading to irrelevant search results,' or 'There's no easy way to save favorite items for later.'</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>6. Brainstorm Possible Solutions</h2>\
        <p class='text-gray-300'>Once pain points are clear, brainstorm a range of potential solutions. Don't limit yourself initially; think broadly from simple tweaks to innovative new features. After brainstorming, evaluate each idea for its feasibility (technical, resource, time), alignment with the product's mission, and potential measurable impact on users and business. This often involves discussing trade-offs.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>7. Define a Product Vision</h2>\
        <p class='text-gray-300'>Before prioritizing specific features, articulate a concise product vision or a 'north star' statement. This summarizes the overarching goal of your proposed design. Example: 'Our product vision is to create a mobile-first trail finder that empowers users of all experience levels to easily discover and navigate personalized hiking routes, fostering a community through social recommendations.'</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>8. Prioritize Features</h2>\
        <p class='text-gray-300'>Given your brainstormed solutions, prioritize which features to build first, especially for an Minimum Viable Product (MVP). Use common frameworks like RICE (Reach, Impact, Confidence, Effort) or MoSCoW (Must have, Should have, Could have, Won't have for now). Select features that deliver significant value quickly, address critical pain points, and allow for learning and iteration. Clearly explain your prioritization rationale.</p>\
        <hr class='my-4 border-gray-700'>\
\
        <h2 class='text-xl font-semibold text-gray-50'>9. Success Metrics</h2>\
        <p class='text-gray-300'>Define how you will measure the success of your proposed design. Choose relevant metrics that align with your product vision and address the pain points you aimed to solve. Consider a mix of quantitative (e.g., engagement rate, retention rate, task completion rate, conversion rate) and qualitative (e.g., Net Promoter Score (NPS), user feedback) metrics. Differentiate between initial MVP success metrics and long-term full rollout metrics.</p>\
    </div>"
    },
    {
    "title": "Sample product design question for [company]",
    "completed": false,
    "summary": "This section generates company-specific product design questions, leveraging the provided job role and product domain. This helps you tailor your practice to scenarios directly relevant to the company you're interviewing with.",
    "content": "This card helps simulate questions aligned to the company and industry you’re targeting. Tailor your prep based on actual user groups and business context.",
    "htmlContent": "\
    <div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
        <h2 class='text-xl font-semibold text-gray-50'>Sample Product Design Question for [Company]</h2>\
        <p class='text-gray-300'>“Imagine [Company] is looking to enhance its B2B SaaS platform for project management. Design a new feature or significant improvement that helps team leads better manage cross-functional dependencies and potential bottlenecks in large-scale projects.”</p>\
\
        <h2 class='text-xl font-semibold text-gray-50'>What This Tests</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>User Empathy:</span> Your ability to understand the complex needs and pain points of team leads and project managers in a B2B context.</li>\
            <li><span class='font-medium'>System Thinking:</span> How you balance various factors like project complexity, team communication, and reporting within a SaaS platform.</li>\
            <li><span class='font-medium'>Problem Solving:</span> Your approach to identifying and addressing critical pain points related to project dependencies and bottlenecks.</li>\
            <li><span class='font-medium'>Definition of Success:</span> How you would define and measure the success of such a feature, considering both user adoption and business impact (e.g., project completion rates, efficiency gains).</li>\
        </ul>\
    </div>"
    },
    {
    "title": "Sample product design question for [industry]",
    "completed": false,
    "summary": "This section focuses on creating industry-aligned design prompts. It tests your ability to apply general product design knowledge in specific industry contexts, relevant to your job goals and target customer needs.",
    "content": "Great for practicing industry-specific scenarios like edtech, fintech, healthtech, etc., aligned with job goals and customer needs.",
    "htmlContent": "\
    <div class='p-4 rounded-xl shadow-md space-y-6 bg-[#08090A] text-gray-200'>\
        <h2 class='text-xl font-semibold text-gray-50'>Industry-Aligned Design Prompt: Healthtech</h2>\
        <p class='text-gray-300'>“Design a digital solution (e.g., a mobile app feature or a standalone platform) to help elderly patients, who may have limited digital literacy, consistently track their medications and dosage compliance at home, especially in areas with limited internet connectivity.”</p>\
\
        <h2 class='text-xl font-semibold text-gray-50'>Why This Is Relevant</h2>\
        <ul class='list-none space-y-2 text-gray-300'>\
            <li><span class='font-medium'>User Segmentation and Prioritization:</span> This requires you to carefully consider the specific needs of elderly users and prioritize features for ease of use and accessibility.</li>\
            <li><span class='font-medium'>Creativity Under Constraints:</span> It tests your ability to innovate solutions while working within significant constraints like low digital literacy and intermittent connectivity.</li>\
            <li><span class='font-medium'>Demands Practical Definition of Success and Trade-offs:</span> You'll need to define what success looks like for medication adherence and discuss the trade-offs involved in designing for accessibility and reliability in challenging environments.</li>\
            <li><span class='font-medium'>Ethical Considerations:</span> It implicitly touches on the importance of privacy and data security in health-related applications.</li>\
        </ul>\
    </div>"
    }
]
}
'''
)
    return product_design

def quick_guide_fun(data):
    quick_guide = (f'''
                  Analyse all {data}
----
 ### ROLE
**VERY VERY IMPORTANT YOU HAVE TO GIVE RESULT IN HTML **div format** only with **tailwind clases** class only**
You are an expert interview preparation coach specializing in Product Manager roles. Your task is to create a concise, actionable Quick Guide that a PM candidate can review in ~15 minutes before their interview.
<div class="px-6 py-4 space-y-6 text-sm bg-white text-gray-800">

  <h1 class="text-3xl font-bold text-gray-900 border-b-4 border-gray-300 pb-2">
    QUICK GUIDE: [Company Name] - [Job Title]
  </h1>

  <div class="space-y-4">
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      KEY FACTS
    </h2>
    <p class="text-gray-700 leading-relaxed">
      [2-3 natural sentences about the company: what it is, what it does, where it's based, major sectors/product lines]
    </p>
  </div>

  <div class="space-y-4">
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      PRODUCT/AREA FOCUS <!-- only include if successfully identified -->
    </h2>
    <ul class="list-disc list-inside space-y-1 text-gray-700">
      <li><strong>What it is:</strong> [1 sentence description]</li>
      <li><strong>Key users:</strong> [Who uses it - 1 sentence]</li>
      <li><strong>Your angle:</strong> [How candidate's experience connects - 1 sentence based on resume analysis]</li>
      <li>[Optional 4th bullet if relevant metric or positioning available]</li>
    </ul>
  </div>

  <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
    INTERVIEW QUESTIONS BY ROUND
  </h2>

  <div class="space-y-4">
    <h3 class="text-lg font-bold text-gray-800">ROUND 1: RECRUITER SCREEN</h3>
    <ul class="list-none space-y-2">
      <li>
        <strong class="text-gray-900">Q:</strong> [Question 1]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Question 2]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Question 3]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Question 4]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Question 5]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
    </ul>
  </div>

  <div class="space-y-4">
    <h3 class="text-lg font-bold text-gray-800">ROUND 2: RESUME DEEP DIVE</h3>
    <ul class="list-none space-y-2">
      <li>
        <strong class="text-gray-900">Q:</strong> [Question 1 based on resume]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Question 2 based on resume]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Question 3 based on resume]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Question 4 based on resume]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Question 5 based on resume]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
    </ul>
  </div>

  <div class="space-y-4">
    <h3 class="text-lg font-bold text-gray-800">ROUND 3: PRODUCT SENSE</h3>
    <ul class="list-none space-y-2">
      <li>
        <strong class="text-gray-900">Q:</strong> [Company-specific product question 1]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Product sense question 2]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Product sense question 3]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Product sense question 4]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Product sense question 5]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
    </ul>
  </div>

  <div class="space-y-4">
    <h3 class="text-lg font-bold text-gray-800">ROUND 4: SITUATION-BASED</h3>
    <ul class="list-none space-y-2">
      <li>
        <strong class="text-gray-900">Q:</strong> [Situation-based question 1 from LP framework]
        <p class="text-gray-700 ml-4">→ Use STAR: Situation → Task → Action (most detail) → Result + Learning</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Situation-based question 2 from LP framework]
        <p class="text-gray-700 ml-4">→ [1-line framework guidance]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Situation-based question 3 from LP framework]
        <p class="text-gray-700 ml-4">→ [1-line framework guidance]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Situation-based question 4 from LP framework]
        <p class="text-gray-700 ml-4">→ [1-line framework guidance]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Situation-based question 5 from LP framework]
        <p class="text-gray-700 ml-4">→ [1-line framework guidance]</p>
      </li>
    </ul>
  </div>

  <div class="space-y-4">
    <h3 class="text-lg font-bold text-gray-800">ROUND 5: BEHAVIORAL</h3>
    <ul class="list-none space-y-2">
      <li>
        <strong class="text-gray-900">Q:</strong> [Behavioral question 1]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Behavioral question 2]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Behavioral question 3]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Behavioral question 4]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
      <li>
        <strong class="text-gray-900">Q:</strong> [Behavioral question 5]
        <p class="text-gray-700 ml-4">→ [1-line guidance or key talking point]</p>
      </li>
    </ul>
  </div>

</div>''')
    return quick_guide