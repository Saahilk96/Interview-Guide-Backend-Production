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
      "summary": "string (Engaging paragraph summarizing the company overview section) atleast of 54 words",
      "content": "string (3–4 fluent sentences explaining the scope and value of this module) ",
      "htmlContent": "
        <div class='p-4 rounded-lg shadow-md bg-white'>
          <h3 class='text-lg font-semibold mb-2'>Company Snapshot</h3>
          <p class='mb-4'>String (3–4 sentence summary explaining what the company does, core product/service, key innovation, and relevance)</p>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Mission & Values</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>Mission: string (Mission of the company. Must be sourced, not inferred.)</li>
            <li>Vision: string (Vision of the company. Must be sourced, not inferred.)</li>
            <li>Values/Principles: string, string, string (List of values/Principles; must be sourced, not inferred.)</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Founding Team</h3>
          <p>String (In 1-2 sentences, state the year company_name was founded and list all the names e.g. name(job title) of its founders entirely from web search) e.g. The founders of company_name are name1(job title), name2(job title), name3(job title),etc.</p>
        </div>
      "
    },
    {
      "title": "Products & Services",
      "completed": false,
      "summary": "string (Summary explaining the company's product/service range and importance) ",
      "content": "string (3–4 fluent sentences describing key offerings and how they help customers) ",
      "htmlContent": "
        <div class='p-4 rounded-lg shadow-md bg-white'>
          <h3 class='text-lg font-semibold mb-2'>Product & Service List</h3>
          <ul class='list-none space-y-2'>
            <li><b>Product/Service A:</b> string (Concise 1-2 sentence description of what it is and does)</li>
            <li><b>Product/Service B:</b> string (Same format, repeat as needed)</li>
          </ul>
        </div>
      "
    },
    {
      "title": "Business Model & Company Financials",
      "completed": false,
      "summary": "string (Summary explaining how the company makes money, growth trajectory, and financial standing) ",
      "content": "string (3–4 fluent sentences on business model, recent funding, and revenue highlights) ",
      "htmlContent": "
        <div class='p-4 rounded-lg shadow-md bg-white'>
          <h3 class='text-lg font-semibold mb-2'>Business Model & Monetization</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (e.g., 'Subscription-based SaaS platform for enterprise analytics')</li>
            <li>String (e.g., 'Freemium pricing for individual users with tiered enterprise plans')</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Financials & Funding</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (Detail of a specific funding event or relevant financial milestone. Examples: 'Series C – $120M – May 2023 – led by Sequoia' OR 'IPO: NASDAQ (TICKER) - Aug 2020, raised $500M' OR 'Post-IPO debt financing - $200M - Jan 2024')</li>
            <li>String (Further funding details or milestones as applicable, following similar formats)</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Revenue</h3>
          <p>Latest available revenue: string (e.g., '$210M in 2023' or 'Revenue not publicly available')</p>
        </div>
      "
    },
    {
      "title": "Target Market & Customers",
      "completed": false,
      "summary": "string (Summary of target market, customer needs, and how the company addresses them) ",
      "content": "string (3–4 sentences describing customers, problems solved, and value delivered) ",
      "htmlContent": "
        <div class='p-4 rounded-lg shadow-md bg-white'>
          <h3 class='text-lg font-semibold mb-2'>Primary Customer Segments</h3>
          <p class='mb-4'>String (3–5 sentences on key industries, sectors, or personas served)</p>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Key Customer Challenges Solved</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (List of core problems solved by the company’s products/services)</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Key Reasons Customers Choose</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (1–2 sentence point on USP 1)</li>
            <li>String (USP 2)</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Notable Clients</h3>
          <ul class='list-none space-y-1'>
            <li>Client 1</li>
            <li>Client 2</li>
          </ul>
        </div>
      "
    },
    {
      "title": "Competitive Landscape",
      "completed": false,
      "summary": "string (Summary outlining competitors and what gives the company an edge or poses a risk) ",
      "content": "string (3–4 sentences describing competitors, strengths, differentiators, and risks) ",
      "htmlContent": "
        <div class='p-4 rounded-lg shadow-md bg-white'>
          <h3 class='text-lg font-semibold mb-2'>Main Competitors</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>Competitor A</li>
            <li>Competitor B</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Key Differentiators (USPs)</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (Point 1)</li>
            <li>String (Point 2)</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Competitive Strengths</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (e.g., 'Proprietary AI engine that automates analysis 30% faster')</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Potential Weaknesses/Challenges</h3>
          <ul class='list-none space-y-1'>
            <li>String (e.g., 'Limited geographic reach compared to global competitors')</li>
          </ul>
        </div>
      "
    },
    {
      "title": "Organization Structure & Leadership",
      "completed": false,
      "summary": "string (Summary describing size, structure, and leadership team of the company) ",
      "content": "string (3–4 sentences about leadership, company structure, and global footprint) ",
      "htmlContent": "
        <div class='p-4 rounded-lg shadow-md bg-white'>
          <h3 class='text-lg font-semibold mb-2'>Size, Status & Location</h3>
          <p class='mb-4'>String (e.g., 'Approx 1,500 employees, private company, HQ in San Francisco, regional offices in London and Bangalore')</p>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Organizational Structure</h3>
          <p class='mb-4'>String (e.g., 'Wholly-owned subsidiary of XYZ Group, with 3 business divisions: Consumer, Enterprise, Research')</p>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Key Leadership</h3>
          <ul class='list-none space-y-1'>
            <li>CEO: Full Name</li>
            <li>CPO: Full Name</li>
            <li>CTO: Full Name</li>
            <li>Other Key Heads: Role – Name</li>
          </ul>
        </div>
      "
    },
    {
      "title": "Industry Context, News & Trends",
      "completed": false,
      "summary": "string (Summary highlighting industry trends, company alignment, and recent developments) ",
      "content": "string (3–4 sentences about the market environment and what the company has recently done to adapt or lead) ",
      "htmlContent": "
        <div class='p-4 rounded-lg shadow-md bg-white'>
          <h3 class='text-lg font-semibold mb-2'>Key Industry Trends</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>Trend 1</li>
            <li>Trend 2</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Recent News & Key Developments</h3>
          <ul class='list-none space-y-1'>
            <li>Event 1: string (e.g., 'Acquired Company Y, expanding its market presence in Asia, in Q3 2023')</li>
            <li>Event 2: string (Description of another significant event)</li>
          </ul>
        </div>
      "
    }
  ],
  "questions":"You are an expert interviewer. Your task is to generate relevant and insightful interview questions for a candidate applying for a [job_role] position at [company]. **IMPORTANT:** Do not generate any answers, only the questions. Please generate 5-7 distinct interview questions that cover a range of areas crucial for evaluating a candidate for this role. These should include: * **Company Knowledge & Alignment:** Questions that assess their understanding of [company]'s business model, mission, values, and how their aspirations align. * **Role-Specific Skills & Experience:** Questions tailored to the core responsibilities and technical or functional skills required for a [job_role]. * **Behavioral & Situational Scenarios:** Questions that uncover their problem-solving abilities, teamwork experience, leadership potential, and how they handle challenges or setbacks. * **Industry & Future Trends:** Questions about current trends, challenges, or the future direction of the industry relevant to [company] and the [job_role]'s field. Ensure all questions are open-ended, designed to encourage detailed and thoughtful responses. --- **Replace `[company]` with the actual company name** (e.g., "Google", "Microsoft", "Tata Consultancy Services") and **`[job_role]` with the specific job role** (e.g., "Software Engineer", "Marketing Manager", "Data Scientist")."
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
    "summary": "string (Engaging paragraph summarizing the Primary Focus Product's core identity, its target market, and its competitive edge, based on information from the company website.) ",
    "content": "string (3–4 fluent sentences explaining what this card covers about the product's foundational aspects and its standing in the market, emphasizing details from official sources.) ",
    "htmlContent": "
        <div class='p-4 rounded-lg shadow-md bg-white'>
          <h3 class='text-lg font-semibold mb-2'>What Core Product Does</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (Concise overview of the product's primary function and capabilities, e.g., 'An advanced analytics platform for processing and visualizing large datasets.') </li>
            <li>String (The main activity or process it enables for users, according to the company website.) </li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Primary Target Market Segment</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (The specific market or industry category the product primarily serves, e.g., 'Enterprise B2B SaaS companies,' as defined on the company website.) </li>
            <li>String (Further details on the segment if available, e.g., 'Focuses on medium to large enterprises within the financial services and healthcare sectors.') </li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Key Problem(s) It Solves for Users</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (Top critical user pain point or business challenge the product resolves, as highlighted on the company website.) </li>
            <li>String (Another significant problem it addresses, or details on how it provides a solution.) </li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Unique Value Proposition (UVP)</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (The core, compelling reason customers choose this product over alternatives, using language from the company website.) </li>
            <li>String (The most significant benefit or outcome it distinctively delivers, if stated on the company website.) </li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Key Differentiators</h3>
          <ul class='list-none space-y-1'>
            <li>String (A standout aspect - feature, technology, etc. - that sets it apart, as presented on the company website.) </li>
            <li>String (Another key differentiator, e.g., 'Offers [Unique Aspect A], unlike most competitors who focus on [Common Aspect B].') </li>
          </ul>
        </div>
      "
    },
    {
    "title": "Core Functionality & Value",
    "completed": false,
    "summary": "string (Summary explaining the Primary Focus Product's key features, the technology powering it, how it integrates, and its monetization model, all based on company website information.) ",
    "content": "string (3–4 fluent sentences describing the product's core mechanics – what it does, what it's built on if strategic, and how it makes money, emphasizing details from official sources.) atleast of 54 words",
    "htmlContent": "
        <div class='p-4 rounded-lg shadow-md bg-white'>
          <h3 class='text-lg font-semibold mb-2'>Identified Product Features & Descriptions</h3>
          <ul class='list-none space-y-2 mb-4'>
            <li><b>Feature 1: [Feature Name]</b> - String (A 1-2 line summary of what the feature does and its primary user benefit or value, as described on the company website.) atleast of 54 words</li>
            <li><b>Feature 2: [Feature Name]</b> - String (Similar detailed description for another feature.) atleast of 54 words</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Key Underlying Technology</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (Description of specific technology fundamental to its performance or UVP, if detailed on the company website, e.g., 'Leverages proprietary machine learning models for advanced predictive analytics.') atleast of 54 words</li>
            <li>String (If standard tech or not detailed, statement like 'Built on a robust and scalable modern tech stack, focusing on reliable delivery of features,' or 'Specific underlying technology details are not highlighted on the website.') atleast of 54 words</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Integration & Ecosystem Synergy</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (Key integrations critical to user workflows, e.g., with other company products or essential third-party services, as mentioned on the company website.) atleast of 54 words</li>
            <li>String (How these integrations extend functionality or streamline user experience, e.g., 'Offers seamless data synchronization with [Contextual Product], enabling a unified workflow for X and Y,' based on website details.) atleast of 54 words</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Monetization Strategy & Pricing Approach</h3>
          <ul class='list-none space-y-1'>
            <li>String (How the product generates revenue, e.g., 'Tiered subscription model: Basic, Pro, Enterprise,' as stated on the company website.) atleast of 54 words</li>
            <li>String (Brief overview of its pricing model or common tiers, e.g., 'Pricing is per user per month, with volume discounts for larger teams,' if available on the website. If not, state that pricing details are not publicly available on the site.) atleast of 54 words</li>
          </ul>
        </div>
      "
    },
    {
    "title": "User Focus & Core Needs",
    "completed": false,
    "summary": "string (Summary of the Primary Focus Product's target users, how they engage with it, and the fundamental needs it meets, based on company website information.) atleast of 54 words",
    "content": "string (3–4 sentences describing who uses the product, what they achieve with it, and the core problems or aspirations it addresses, emphasizing details from official sources.) atleast of 54 words",
    "htmlContent": "
        <div class='p-4 rounded-lg shadow-md bg-white'>
          <h3 class='text-lg font-semibold mb-2'>Primary Target User Profile(s)</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (Detailed description of the most important user segment or persona, e.g., 'Marketing Managers in mid-sized technology companies requiring advanced campaign analytics,' as defined on the company website.) atleast of 54 words</li>
            <li>String (Key characteristics, roles, daily tasks, and motivations of another primary user profile relevant to the product, based on website information.) atleast of 54 words</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>How Users Engage with the Product</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (Scenario 1: Description of a common workflow or task a user performs with the product, e.g., 'To optimize ad spend, a user first ingests campaign data from multiple sources, then utilizes the platform's attribution modeling feature to identify high-performing channels, and finally generates a comprehensive report for stakeholders.') atleast of 54 words</li>
            <li>String (Scenario 2: Similar detailed description for another key interaction or use case, as described or inferred from the company website.) atleast of 54 words</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Fundamental User Needs Addressed</h3>
          <ul class='list-none space-y-1'>
            <li>String (A core underlying need or 'job' the product helps users accomplish, e.g., 'To gain actionable insights from complex datasets to make data-driven business decisions,' inferred from website information.) atleast of 54 words</li>
            <li>String (Another fundamental need or aspiration the product fulfills, framed as the progress users are trying to make, e.g., 'To streamline collaborative project management and improve team productivity on complex initiatives.') atleast of 54 words</li>
          </ul>
        </div>
      "
    },
    {
    "title": "Competitive Landscape (Product-Focused)",
    "completed": false,
    "summary": "string (Summary outlining the Primary Focus Product's main competitors and how it differentiates itself within its specific market, based on website info and supplemented by general knowledge where stated.) atleast of 54 words",
    "content": "string (3–4 sentences describing direct and indirect competitors, and the product's strategic positioning against them, emphasizing details from official sources where possible.) atleast of 54 words",
    "htmlContent": "
        <div class='p-4 rounded-lg shadow-md bg-white'>
          <h3 class='text-lg font-semibold mb-2'>Key Direct Competitors</h3>
          <ul class='list-none space-y-2 mb-4'>
            <li><b>Competitor A: [Name].</b> String (Known for [Their main strength/focus area]. If competitor details are from general knowledge, state so. If from company website, cite that.) atleast of 54 words</li>
            <li><b>Competitor B: [Name].</b> String (Similar detailed description for another direct competitor and its known strengths.) atleast of 54 words</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Indirect Competition & Alternative Solutions</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (Other ways users currently address the core problem the Primary Focus Product solves, e.g., 'Utilizing generic spreadsheet software for data analysis, which lacks specialized features but is widely accessible,' inferred from product descriptions or general market understanding.) atleast of 54 words</li>
            <li>String (Description of another alternative solution or type of indirect competitor, e.g., 'Developing custom in-house tools, which offer tailored functionality but require significant development resources and ongoing maintenance.') atleast of 54 words</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Positioning Against Competitors</h3>
          <ul class='list-none space-y-1'>
            <li>String (How the product aims to win against direct competitors, e.g., 'By offering a more intuitive user interface and significantly faster data processing speeds, as highlighted by its UVP and differentiators from the company website.') atleast of 54 words</li>
            <li>String (Its key competitive advantage in the current landscape, e.g., 'Its unique focus on seamless integration with the broader [Company Name] ecosystem provides a unified user experience not easily matched by standalone competitors.') atleast of 54 words</li>
          </ul>
        </div>
      "
    },
    {
    "title": "SWOT Analysis",
    "completed": false,
    "summary": "string (Summary of the Primary Focus Product's internal strengths and weaknesses, and the external opportunities and threats it faces, based on website information and general market knowledge.) atleast of 54 words",
    "content": "string (3–4 sentences providing a balanced overview of the product's strategic position based on the SWOT factors, emphasizing details from official sources for S & W.) atleast of 54 words",
    "htmlContent": "
        <div class='p-4 rounded-lg shadow-md bg-white'>
          <h3 class='text-lg font-semibold mb-2'>Strengths</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (A key internal advantage, e.g., 'Leverages [Company Name]'s strong brand reputation and existing enterprise customer base for market penetration,' derived from website and JD analysis.) atleast of 54 words</li>
            <li>String (Another core competency, e.g., 'Possesses proprietary algorithms for [specific function] that deliver demonstrably superior accuracy compared to alternatives, as evidenced by case studies on the company website.') atleast of 54 words</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Weaknesses</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (An internal limitation, e.g., 'The product currently has a steeper learning curve for non-technical users, potentially hindering wider adoption in certain segments,' inferred cautiously from website or JD.) atleast of 54 words</li>
            <li>String (Another area for improvement, e.g., 'Perceived as having a higher price point compared to some newer, more narrowly focused competitors, which could be a barrier for smaller businesses.') atleast of 54 words</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Opportunities</h3>
          <ul class='list-none space-y-1 mb-4'>
            <li>String (A significant external market opportunity, e.g., 'The rapidly growing market demand for AI-powered automation in [target industry] presents a significant expansion opportunity for the product’s advanced capabilities.') atleast of 54 words</li>
            <li>String (Another potential opportunity, e.g., 'The increasing need for robust data privacy and compliance features offers a chance to further differentiate by enhancing its existing security architecture.') atleast of 54 words</li>
          </ul>
          <hr class='my-4'>
          <h3 class='text-lg font-semibold mb-2'>Threats</h3>
          <ul class='list-none space-y-1'>
            <li>String (A key external threat, e.g., 'Intense competition from both established players and agile startups introducing innovative features at a rapid pace, requiring continuous product development.') atleast of 54 words</li>
            <li>String (Another potential challenge, e.g., 'Potential shifts in technology standards or user preferences towards open-source alternatives could impact long-term market share if not proactively addressed.') atleast of 54 words</li>
          </ul>
        </div>
      "
    }
    ],
    "questions":"You are an expert product analyst and interviewer. Your task is to generate a set of relevant and insightful product research questions for a thorough analysis of [product_name]. **IMPORTANT:** Do not generate any answers; provide only the questions. Please generate 5-7 distinct questions that cover the following areas of product research: * **Problem and User Value:** Questions about the core problem the product solves, its target users, and the value it delivers. * **Competitive Landscape:** Questions focused on how the product stands out from competitors. * **Feature Analysis & Prioritization:** Questions about existing features, their effectiveness, and potential future improvements. * **Risks and Challenges:** Questions that explore potential obstacles to the product's success. Ensure the questions are open-ended and designed to elicit detailed, analytical responses from a product expert. --- **Replace `[product_name]` with the actual name of the product you want to analyze** (e.g., "Google Maps", "Slack", "Netflix", "ChatGPT")."
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
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "htmlContent":"
        Primary Mission / Underlying Need

information description 1

information description 2

...

Key Responsibility Areas & PM Activities

information description 1

information description 2

...

Areas of Specific Emphasis or Complexity

information description 1

information description 2

...

some main title

information description 1

information description 2

...

some main title

information description 1

information description 2

...

some main title

information description 1

information description 2

...
        "
        },
        {
        "title": "Required Skills & Experience",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "htmlContent":"
        Essential Hard Skills / Technical Requirements

information description 1

information description 2

...

Critical Soft Skills & Attributes

information description 1

information description 2

...

Required Experience Level & Domain

information description 1

information description 2

...

Preferred / Standout Qualifications

information description 1

information description 2

...


        "
        },
        {
        "title": "Defining Success & Measuring Impact",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "htmlContent":"
        Explicitly Stated Success Metrics / KPIs

information description 1

information description 2

...

Implied Success Indicators

information description 1

information description 2

...

Expected Business / Product Impact

information description 1

information description 2

...

Connecting Success to Interview Examples

information description 1

information description 2

...
        "
        },
        {
        "title": "Team, Collaboration & Reporting Structure",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "htmlContent":"
        Reporting Structure

information description 1

information description 2

...

Key Internal Collaborators / Stakeholders

information description 1

information description 2

...

Key External Collaborators / Relationships

information description 1

information description 2

...

Implied Collaboration Style & Potential Challenges

information description 1

information description 2

...
        "
        },
        {
        "title": "Strategic Context & Role Significance",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "htmlContent":"
        The Company's Need for this Role

information description 1

information description 2

...

Contribution to Broader Product / Company Strategy

information description 1

information description 2

...

Potential Strategic Challenges or Opportunities

information description 1

information description 2

...

Role Autonomy and Influence Level

information description 1

information description 2

...
        "
        },
         {
        "title": "Key Themes & Interview Angles",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "htmlContent":"
        Overarching Themes & Priorities

information description 1

information description 2

...

Areas Likely to be Deeply Probed

information description 1

information description 2

...

How to Align Your Experience

information description 1

information description 2

...

Insightful Questions to Ask

information description 1

information description 2

...
        "
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
    "summary": "a full summary text of some long length that summarizes all these modules",
    "content": "some full long information text",
    "htmlContent":"
    Highly Relevant Technical Skills

information description 1

information description 2

...

Business/Domain Knowledge Fit

information description 1

information description 2

...

Experience That Matches Scope

information description 1

information description 2

...

Team/Collaboration Readiness

information description 1

information description 2

...

Communication or Leadership Strengths

information description 1

information description 2

...

Unique Background or Edge

information description 1

information description 2

...
    "
    },
    {
    "title": "Potential Gaps & How to Address",
    "completed": false,
    "summary": "a full summary text of some long length that summarizes all these modules",
    "content": "some full long information text",
    "htmlContent":"
    Missing Specific Tool/Technology Experience

information description 1

information description 2

...

Shorter Duration in Similar Roles

information description 1

information description 2

...

Limited Exposure to Certain Business Models

information description 1

information description 2

...

Ways to Frame Transferable Skills

information description 1

information description 2

...
    "
    },
    {
    "title": "Standout Experiences to Highlight",
    "completed": false,
    "summary": "a full summary text of some long length that summarizes all these modules",
    "content": "some full long information text",
    "htmlContent":"
    Project/Initiative 1 (Title/Context)

information description 1

information description 2

...

Project/Initiative 2 (Title/Context)

information description 1

information description 2

...

Impactful Experience 3 (Title/Context)

information description 1

information description 2

...

Unique Contribution or Edge

information description 1

information description 2

...
    "
    }
]
}
    ''')
    return resume_experience_to_highlight_to_stand_out

def recruiter_screen_preparation_fun(data):
    recruiter_screen_preparation =  (f'''Analyse this entire {data}'''

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

{{
"quick_summary": "This module equips candidates with a recruiter-specific prep strategy based on the JD provided. It outlines expected recruiter screening goals, provides quick facts, helps shape a tailored self-introduction, anticipates common recruiter questions, and suggests thoughtful questions the candidate should ask. All content is structured to boost candidate clarity, confidence, and conversational readiness in early-stage calls.",
"sub_modules": [
    {{
    "title": "Call Rubric & Quick Facts",
    "completed": false,
    "summary": "This card describes the purpose and structure of the recruiter screen, offering a clear view of how the candidate will be evaluated. It summarizes what recruiters typically look for, and extracts JD-specific logistics like salary and location when available.",
    "content": "A comprehensive breakdown of call goals, key fit checks, and recruiter-facing evaluation themes.",
    "htmlContent":"
    <div class='p-4 rounded-lg shadow-md bg-white space-y-4'>
        <h2 class='text-lg font-semibold'>Purpose of the Recruiter Screen</h2>
        <p>To assess candidate's fit for the role based on qualifications, communication skills, enthusiasm, and logistical alignment with job requirements.</p>
        <hr class='my-4'>
        
        <h2 class='text-lg font-semibold'>Key Evaluation Areas</h2>
        <ul class='list-disc list-inside space-y-1'>
            <li>Clear articulation of relevant skills and experience</li>
            <li>Demonstrated interest in the role/company</li>
            <li>Matching salary and location preferences</li>
        </ul>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Salary Information from JD</h2>
        <p>Salary information not provided in the JD.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Location & Remote Status from JD</h2>
        <p>Location/remote status unclear from JD.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Other Logistical Details</h2>
        <p>No specific logistical or compliance constraints mentioned in the JD.</p>
    </div>"
    }},
    {{
    "title": "Craft Your Introduction",
    "completed": false,
    "summary": "Provides a tailored framework to deliver a concise, compelling self-introduction aligned with JD expectations. It helps connect the candidate’s background with what the recruiter is likely listening for.",
    "content": "This card empowers the candidate to deliver a confident 'Tell me about yourself' answer using the Past-Present-Future model.",
    "htmlContent":"
    <div class='p-4 rounded-lg shadow-md bg-white space-y-4'>
        <h2 class='text-lg font-semibold'>Strategy for Tailoring Your Pitch</h2>
        <p>Use the Past-Present-Future framework to keep your intro structured and relevant. Reference JD themes like tools, collaboration, or results.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Key Elements to Highlight (Based on JD)</h2>
        <ul class='list-disc list-inside space-y-1'>
            <li>Experience managing projects aligned with the job’s scope</li>
            <li>Skills related to team collaboration or tools listed in the JD</li>
        </ul>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Connecting Your Experience</h2>
        <p>Use keywords directly from the JD. For example, if it mentions cross-functional work, highlight that using similar phrases in your pitch.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Practice and Timing</h2>
        <p>Keep your pitch 2-3 minutes, and rehearse for clarity and confidence.</p>
    </div>"
    }},
    {{
    "title": "Insightful Questions to Ask",
    "completed": false,
    "summary": "Guides the candidate on what to ask the recruiter to demonstrate interest and get clarity on the role and company. These questions reflect curiosity, preparation, and JD awareness.",
    "content": "Prepares a set of smart, strategic questions to ask the recruiter, categorized for ease of access during the call.",
    "htmlContent":"
    <div class='p-4 rounded-lg shadow-md bg-white space-y-4'>
        <h2 class='text-lg font-semibold'>Questions About the Role & Team</h2>
        <ul class='list-disc list-inside space-y-1'>
            <li>What are the immediate priorities for this role in the first 3 months?</li>
            <li>Can you tell me more about the team I’ll be working with?</li>
        </ul>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Interview Process</h2>
        <ul class='list-disc list-inside space-y-1'>
            <li>What does the rest of the interview process look like?</li>
            <li>How soon are you looking to fill the role?</li>
        </ul>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Culture and Team Environment</h2>
        <ul class='list-disc list-inside space-y-1'>
            <li>How would you describe the team culture?</li>
            <li>What traits do successful team members usually have?</li>
        </ul>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Clarifying JD Details</h2>
        <p>Could you help clarify what “strategic impact” refers to in the JD responsibilities?</p>
    </div>"
    }}
]
}}
''')
    return recruiter_screen_preparation

def favorite_product_question_fun(data):
    favorite_product_question = (f'''Analyse this entire {data}'''

'''
----
This module helps you confidently answer one of the most common product management interview questions — “What’s your favorite product and how would you improve it?” It breaks down interviewer intent, question types, and gives a powerful 5-step framework to structure your response with depth and clarity.

----
Give me response in this JSON format only and do not include any asterisk symbols in htmlContent:

{{
"quick_summary": "This guide offers structured preparation to tackle the popular 'Favorite Product' interview question. It explains the reasoning behind the question, what follow-ups to expect, how to select a meaningful product, and how to suggest intelligent improvements. The second card introduces a 5-step framework to organize your answer clearly, show empathy for users, and demonstrate product thinking in action.",
"sub_modules": [
    {{
    "title": "What’s Your Favorite Product?",
    "completed": false,
    "summary": "Understand why interviewers ask this question and how to navigate its common variations. Learn tips on picking a strong product and framing your improvements thoughtfully.",
    "content": "This module helps demystify a common interview favorite, offering techniques to build a high-impact response grounded in personal insight and structured thinking.",
    "htmlContent":"
    <div class='p-4 rounded-lg shadow-md bg-white space-y-4'>
        <h2 class='text-lg font-semibold'>Why Do Interviewers Ask This?</h2>
        <p>This question is a low-pressure entry point for interviewers to evaluate your product thinking, user empathy, and communication clarity. It helps them see how you analyze product tradeoffs and what types of products you personally connect with.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>What to Expect</h2>
        <p>Typically asked early in interviews. Expect 5–10 minutes of casual conversation with follow-ups like “How would you improve it?” or “How would you measure success?”</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Common Variants</h2>
        <ul class='list-disc list-inside space-y-1'>
            <li>What’s your favorite Google product?</li>
            <li>What’s a product you hate that others love?</li>
            <li>What’s a product with untapped potential?</li>
        </ul>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>How to Choose a Good Product</h2>
        <ul class='list-disc list-inside space-y-1'>
            <li>Pick something you truly care about and have opinions on</li>
            <li>Choose products with meaningful pros and cons</li>
            <li>Avoid direct competitors of the company</li>
            <li>Avoid overly simple or trivial products</li>
        </ul>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Example Product Improvement</h2>
        <p>“One thing I’d improve about Notion is its search experience. I’d introduce a lightweight tagging system that dynamically groups tagged content for easier synthesis.”</p>
    </div>"
    }},
    {{
    "title": "5 Steps Framework",
    "completed": false,
    "summary": "A 5-part structure to craft your answer with clarity: pick a meaningful product, describe it briefly, define users, highlight pain points addressed, and suggest improvements that reflect your thinking.",
    "content": "This framework ensures your response includes product empathy, user-centric thinking, and actionable improvement ideas.",
    "htmlContent":"
    <div class='p-4 rounded-lg shadow-md bg-white space-y-4'>
        <h2 class='text-lg font-semibold'>1. Pick the Right Product</h2>
        <ul class='list-disc list-inside space-y-1'>
            <li>Have 3 digital and 1 physical product ready</li>
            <li>Avoid culturally niche or overly common choices unless you have a unique take</li>
        </ul>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>2. Intro in One Sentence</h2>
        <p>Start with a crisp description: “Waze helps users navigate using real-time traffic data.”</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>3. Define Customer Segments</h2>
        <p>Identify 3–4 user groups. Share which one you relate to most: “As a new parent, I use Waze to avoid long drives with a crying baby.”</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>4. Pain-Driven Features</h2>
        <p>Use the structure: Pain → Feature → Outcome</p>
        <p>Example: “Traffic stresses me with kids in the car → Waze reroutes in real time → I stay calm and get there faster.”</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>5. Suggest Improvements</h2>
        <ul class='list-disc list-inside space-y-1'>
            <li>Align with company mission</li>
            <li>Address unmet user needs</li>
            <li>Add tech-based enhancements</li>
            <li>Improve full journey experience (e.g., media integration)</li>
        </ul>
    </div>"
    }}
]
}}
''')
    return favorite_product_question

def product_design_fun(data):
    product_design = (f'''Analyse this entire {data}'''

'''
----
This module helps candidates master product design interview questions. It includes an overview of what to expect, how to think through structured responses, and practice with example questions aligned to a company's domain or industry.

----
Give me response in this JSON format only and ensure do not use any asterisk symbols anywhere:

{{
"quick_summary": "This comprehensive module prepares you for product design interview questions. It breaks down how to approach these questions, what interviewers evaluate, and how to elevate your response from good to great. You’ll learn a step-by-step framework including clarifying the prompt, identifying users, understanding their pain points, brainstorming solutions, and defining success metrics. It also provides company-specific sample questions to help you simulate real interviews.",
"sub_modules": [
    {{
    "title": "Overview of Product Design Questions",
    "completed": false,
    "summary": "This card provides a foundational understanding of product design interviews. It covers expectations, what interviewers assess, sample responses, and a rubric to distinguish between performance levels.",
    "content": "Get familiar with how product design questions work, why they’re asked, and how to recognize the difference between an average and an outstanding answer.",
    "htmlContent": "
    <div class='p-4 bg-white rounded-lg shadow space-y-4'>
        <h2 class='text-lg font-semibold'>What to Expect</h2>
        <p>Expect open-ended and problem-solving questions such as “Design X for Y” or “Improve Z.” Responses are evaluated on structure, creativity, and user empathy. Follow a flow like: Clarify → Define Users → Pain Points → Solutions → Metrics.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>What Interviewers are Looking For</h2>
        <ul class='list-disc list-inside space-y-1'>
            <li>Product sense and structured thinking</li>
            <li>User empathy and prioritization</li>
            <li>Creativity balanced with feasibility</li>
            <li>Strong communication and decision rationale</li>
        </ul>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Sample Answers: Good vs. Great</h2>
        <p>A “Good” answer may follow structure but lack insight or prioritization. A “Great” answer uses a framework, prioritizes pain points, explains trade-offs, and shows deep user understanding.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Why do companies ask Product Design questions</h2>
        <p>These simulate real-world thinking and pressure handling. They reveal how you define problems, empathize with users, ideate solutions, and think about feasibility and success.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>Evaluation Rubric</h2>
        <p>Interviewers evaluate your answer on framing, structure, creativity, communication, and alignment to user needs. Levels might include Poor (disorganized), Good (structured), and Great (insightful + practical).</p>
    </div>"
    }},
    {{
    "title": "How to Answer Product Design Questions",
    "completed": false,
    "summary": "This card explains a detailed step-by-step framework for approaching product design problems. It helps you build answers that are user-centered, thoughtful, and clear.",
    "content": "Learn the full structure to solve product design questions, starting with clarifying the context and ending with success metrics.",
    "htmlContent": "
    <div class='p-4 bg-white rounded-lg shadow space-y-4'>
        <h2 class='text-lg font-semibold'>1. Clarify and Get Context</h2>
        <p>Ask questions like: Who are we solving for? What's the goal? Is it a mobile or web experience? Clarifying ensures alignment with the interviewer.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>2. Mission/Vision</h2>
        <p>For known companies, tie your solution to their mission. For unknowns, make assumptions and state them clearly.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>3. Define Personas (User Groups)</h2>
        <p>Identify 2–4 user types. Prioritize based on need, frequency of use, and alignment with business goals. Example: “Hikers, casual walkers, and tourists.”</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>4. User Journey</h2>
        <p>Map the user’s flow from start to finish. Example: Search → Filter → View Details → Save → Navigate → Review.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>5. Identify User Pain Points and Opportunities</h2>
        <p>Find friction in the journey (e.g., bad filters or hard navigation). Focus on high-impact problems for MVP.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>6. Brainstorm Possible Solutions</h2>
        <p>Sketch a range of ideas, from simple to innovative. Evaluate them for feasibility, alignment with mission, and measurable impact.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>7. Define a Product Vision</h2>
        <p>Summarize the product’s north star. Example: “A mobile-first trail finder for all experience levels, with social recommendations.”</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>8. Prioritize Features</h2>
        <p>Use frameworks like RICE or MoSCoW. Choose features that deliver value quickly and support learning.</p>
        <hr class='my-4'>

        <h2 class='text-lg font-semibold'>9. Success Metrics</h2>
        <p>Choose metrics like engagement, retention, NPS, or task success rate. Define what success looks like at MVP vs. full rollout.</p>
    </div>"
    }},
    {{
    "title": "Sample product design question for [company]",
    "completed": false,
    "summary": "Generate company-specific product design questions using the job role and product domain. Helps in tailoring your practice to real-world scenarios.",
    "content": "This card helps simulate questions aligned to the company and industry you’re targeting. Tailor your prep based on actual user groups and business context.",
    "htmlContent": "
    <div class='p-4 bg-white rounded-lg shadow space-y-4'>
        <h2 class='text-lg font-semibold'>Sample Product Design Question</h2>
        <p>“Design a platform feature that helps freelancers on [Company]'s platform find better matching projects while minimizing idle time.”</p>

        <h2 class='text-lg font-semibold'>What This Tests</h2>
        <ul class='list-disc list-inside space-y-1'>
            <li>User empathy with freelancers and clients</li>
            <li>Ability to balance search algorithms, recommendations, and UX</li>
            <li>Definition of success from both sides</li>
        </ul>
    </div>"
    }},
    {{
    "title": "Sample product design question for [industry]",
    "completed": false,
    "summary": "This section focuses on creating industry-aligned design prompts. It tests your ability to apply general product design knowledge in specific contexts.",
    "content": "Great for practicing industry-specific scenarios like edtech, fintech, healthtech, etc., aligned with job goals and customer needs.",
    "htmlContent": "
    <div class='p-4 bg-white rounded-lg shadow space-y-4'>
        <h2 class='text-lg font-semibold'>Industry-Aligned Design Prompt</h2>
        <p>“Design a digital solution to help patients track medications and dosage compliance in rural areas with limited connectivity.”</p>

        <h2 class='text-lg font-semibold'>Why This Is Relevant</h2>
        <ul class='list-disc list-inside space-y-1'>
            <li>Requires user segmentation and prioritization</li>
            <li>Tests creativity under constraints</li>
            <li>Demands practical definition of success and trade-offs</li>
        </ul>
    </div>"
    }}
]
}}
''')
    return product_design


