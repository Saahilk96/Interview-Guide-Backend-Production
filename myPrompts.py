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
      "points": [
        {
          "main": "Company Snapshot",
          "subPoints": [
            "String (3–4 sentence summary explaining what the company does, core product/service, key innovation, and relevance)",
            ...
          ]
        },
        {
          "main": "Mission & Values",
          "subPoints": [
            "Mission: string (Mission of the company. Must be sourced, not inferred.)",
            "Vision: string (Vision of the company. Must be sourced, not inferred.)",
            "Values/Principles: [string, string, string] (List of values/Principles; must be sourced, not inferred.)",
            ...
          ]
        },
        {
          "main": "Founding Team",
          "subPoints": [
            "String (In 1-2 sentences, state the *year* company_name was founded and list *all the names* *e.g. name(job title)* of its founders entirely from web search) e.g. *The founders of company_name are name1(job title), name2(job title), name3(job title),etc.*",
            ...
          ]
        }
      ]
    },
    {
      "title": "Products & Services",
      "completed": false,
      "summary": "string (Summary explaining the company's product/service range and importance) ",
      "content": "string (3–4 fluent sentences describing key offerings and how they help customers) ",
      "points": [
        {
          "main": "Product & Service List",
          "subPoints": [
            "Product/Service A: string (Concise 1-2 sentence description of what it is and does)",
            "Product/Service B: string (Same format, repeat as needed)",
            ...
          ]
        }
      ]
    },
    {
      "title": "Business Model & Company Financials",
      "completed": false,
      "summary": "string (Summary explaining how the company makes money, growth trajectory, and financial standing) ",
      "content": "string (3–4 fluent sentences on business model, recent funding, and revenue highlights) ",
      "points": [
        {
          "main": "Business Model & Monetization",
          "subPoints": [
            "String (e.g., 'Subscription-based SaaS platform for enterprise analytics')",
            "String (e.g., 'Freemium pricing for individual users with tiered enterprise plans')",
            ...
          ]
        },
        {
          "main": "Financials & Funding",
          "subPoints": [
            "String (Detail of a specific funding event or relevant financial milestone. Examples: 'Series C – $120M – May 2023 – led by Sequoia' OR 'IPO: NASDAQ (TICKER) - Aug 2020, raised $500M' OR 'Post-IPO debt financing - $200M - Jan 2024')",
            "String (Further funding details or milestones as applicable, following similar formats)",
            ...
          ]
        },
        {
          "main": "Revenue",
          "subPoints": [
            "Latest available revenue: string (e.g., '$210M in 2023' or 'Revenue not publicly available')",
            ...
          ]
        }
      ]
    },
    {
      "title": "Target Market & Customers",
      "completed": false,
      "summary": "string (Summary of target market, customer needs, and how the company addresses them) ",
      "content": "string (3–4 sentences describing customers, problems solved, and value delivered) ",
      "points": [
        {
          "main": "Primary Customer Segments",
          "subPoints": [
            "String (3–5 sentences on key industries, sectors, or personas served)",
            ...
          ]
        },
        {
          "main": "Key Customer Challenges Solved",
          "subPoints": [
            "String (List of core problems solved by the company’s products/services)",
            ...
          ]
        },
        {
          "main": "Key Reasons Customers Choose",
          "subPoints": [
            "String (1–2 sentence point on USP 1)",
            "String (USP 2)",
            "String (USP 3, if applicable)",
            ...
          ]
        },
        {
          "main": "Notable Clients",
          "subPoints": [
            "Client 1",
            "Client 2",
            "Client 3",
            "Client 4",
            "Client 5",
            "Client 6",
            "Client 7",
            ...
          ]
        }
      ]
    },
    {
      "title": "Competitive Landscape",
      "completed": false,
      "summary": "string (Summary outlining competitors and what gives the company an edge or poses a risk) ",
      "content": "string (3–4 sentences describing competitors, strengths, differentiators, and risks) ",
      "points": [
        {
          "main": "Main Competitors",
          "subPoints": [
            "Competitor A",
            "Competitor B",
            "Competitor C",
            "Competitor D",
            "Competitor E",
            "Competitor F",
            "Competitor G",
            ...
          ]
        },
        {
          "main": "Key Differentiators (USPs)",
          "subPoints": [
            "String (Point 1)",
            "String (Point 2)",
            ...
          ]
        },
        {
          "main": "Competitive Strengths",
          "subPoints": [
            "String (e.g., 'Proprietary AI engine that automates analysis 30% faster')",
            ...
          ]
        },
        {
          "main": "Potential Weaknesses/Challenges",
          "subPoints": [
            "String (e.g., 'Limited geographic reach compared to global competitors')",
            ...
          ]
        }
      ]
    },
    {
      "title": "Organization Structure & Leadership",
      "completed": false,
      "summary": "string (Summary describing size, structure, and leadership team of the company) ",
      "content": "string (3–4 sentences about leadership, company structure, and global footprint) ",
      "points": [
        {
          "main": "Size, Status & Location",
          "subPoints": [
            "String (e.g., 'Approx 1,500 employees, private company, HQ in San Francisco, regional offices in London and Bangalore')",
            ...
          ]
        },
        {
          "main": "Organizational Structure",
          "subPoints": [
            "String (e.g., 'Wholly-owned subsidiary of XYZ Group, with 3 business divisions: Consumer, Enterprise, Research')",
            ...
          ]
        },
        {
          "main": "Key Leadership",
          "subPoints": [
            "CEO: Full Name",
            "CPO: Full Name",
            "CTO: Full Name",
            "Other Key Heads: Role – Name",
            ...
          ]
        }
      ]
    },
    {
      "title": "Industry Context, News & Trends",
      "completed": false,
      "summary": "string (Summary highlighting industry trends, company alignment, and recent developments) ",
      "content": "string (3–4 sentences about the market environment and what the company has recently done to adapt or lead) ",
      "points": [
        {
          "main": "Key Industry Trends",
          "subPoints": [
            "Trend 1",
            "Trend 2",
            "Trend 3",
            ...
          ]
        },
        {
          "main": "Recent News & Key Developments",
          "subPoints": [
            "Event 1: string (e.g., 'Acquired Company Y, expanding its market presence in Asia, in Q3 2023')",
            "Event 2: string (Description of another significant event)",
            "Event 3: string (Description of another significant event)",
            "Event 4: string (If applicable)",
            "Event 5: string (If applicable)",
            ...
          ]
        }
      ]
    }
  ]
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
    "points": [
    {
    "main": "What Core Product Does",
    "subPoints": [
    "String (Concise overview of the product's primary function and capabilities, e.g., 'An advanced analytics platform for processing and visualizing large datasets.') ",
    "String (The main activity or process it enables for users, according to the company website.) "
    ]
    },
    {
    "main": "Primary Target Market Segment",
    "subPoints": [
    "String (The specific market or industry category the product primarily serves, e.g., 'Enterprise B2B SaaS companies,' as defined on the company website.) ",
    "String (Further details on the segment if available, e.g., 'Focuses on medium to large enterprises within the financial services and healthcare sectors.') "
    ]
    },
    {
    "main": "Key Problem(s) It Solves for Users",
    "subPoints": [
    "String (Top critical user pain point or business challenge the product resolves, as highlighted on the company website.) ",
    "String (Another significant problem it addresses, or details on how it provides a solution.) "
    ]
    },
    {
    "main": "Unique Value Proposition (UVP)",
    "subPoints": [
    "String (The core, compelling reason customers choose this product over alternatives, using language from the company website.) ",
    "String (The most significant benefit or outcome it distinctively delivers, if stated on the company website.) "
    ]
    },
    {
    "main": "Key Differentiators",
    "subPoints": [
    "String (A standout aspect - feature, technology, etc. - that sets it apart, as presented on the company website.) ",
    "String (Another key differentiator, e.g., 'Offers [Unique Aspect A], unlike most competitors who focus on [Common Aspect B].') "
    ]
    }
    ]
    },
    {
    "title": "Core Functionality & Value",
    "completed": false,
    "summary": "string (Summary explaining the Primary Focus Product's key features, the technology powering it, how it integrates, and its monetization model, all based on company website information.) ",
    "content": "string (3–4 fluent sentences describing the product's core mechanics – what it does, what it's built on if strategic, and how it makes money, emphasizing details from official sources.) atleast of 54 words",
    "points": [
    {
    "main": "Identified Product Features & Descriptions",
    "subPoints": [
    "Feature 1: [Feature Name] - String (A 1-2 line summary of what the feature does and its primary user benefit or value, as described on the company website.) atleast of 54 words",
    "Feature 2: [Feature Name] - String (Similar detailed description for another feature.) atleast of 54 words"
    // Add more feature strings as identified, each trying to meet the word count through detailed description.
    // "Strive to list all distinct features clearly described on the website."
    ]
    },
    {
    "main": "Key Underlying Technology",
    "subPoints": [
    "String (Description of specific technology fundamental to its performance or UVP, if detailed on the company website, e.g., 'Leverages proprietary machine learning models for advanced predictive analytics.') atleast of 54 words",
    "String (If standard tech or not detailed, statement like 'Built on a robust and scalable modern tech stack, focusing on reliable delivery of features,' or 'Specific underlying technology details are not highlighted on the website.') atleast of 54 words"
    ]
    },
    {
    "main": "Integration & Ecosystem Synergy",
    "subPoints": [
    "String (Key integrations critical to user workflows, e.g., with other company products or essential third-party services, as mentioned on the company website.) atleast of 54 words",
    "String (How these integrations extend functionality or streamline user experience, e.g., 'Offers seamless data synchronization with [Contextual Product], enabling a unified workflow for X and Y,' based on website details.) atleast of 54 words"
    ]
    },
    {
    "main": "Monetization Strategy & Pricing Approach",
    "subPoints": [
    "String (How the product generates revenue, e.g., 'Tiered subscription model: Basic, Pro, Enterprise,' as stated on the company website.) atleast of 54 words",
    "String (Brief overview of its pricing model or common tiers, e.g., 'Pricing is per user per month, with volume discounts for larger teams,' if available on the website. If not, state that pricing details are not publicly available on the site.) atleast of 54 words"
    ]
    }
    ]
    },
    {
    "title": "User Focus & Core Needs",
    "completed": false,
    "summary": "string (Summary of the Primary Focus Product's target users, how they engage with it, and the fundamental needs it meets, based on company website information.) atleast of 54 words",
    "content": "string (3–4 sentences describing who uses the product, what they achieve with it, and the core problems or aspirations it addresses, emphasizing details from official sources.) atleast of 54 words",
    "points": [
    {
    "main": "Primary Target User Profile(s)",
    "subPoints": [
    "String (Detailed description of the most important user segment or persona, e.g., 'Marketing Managers in mid-sized technology companies requiring advanced campaign analytics,' as defined on the company website.) atleast of 54 words",
    "String (Key characteristics, roles, daily tasks, and motivations of another primary user profile relevant to the product, based on website information.) atleast of 54 words"
    ]
    },
    {
    "main": "How Users Engage with the Product",
    "subPoints": [
    "String (Scenario 1: Description of a common workflow or task a user performs with the product, e.g., 'To optimize ad spend, a user first ingests campaign data from multiple sources, then utilizes the platform's attribution modeling feature to identify high-performing channels, and finally generates a comprehensive report for stakeholders.') atleast of 54 words",
    "String (Scenario 2: Similar detailed description for another key interaction or use case, as described or inferred from the company website.) atleast of 54 words"
    ]
    },
    {
    "main": "Fundamental User Needs Addressed",
    "subPoints": [
    "String (A core underlying need or 'job' the product helps users accomplish, e.g., 'To gain actionable insights from complex datasets to make data-driven business decisions,' inferred from website information.) atleast of 54 words",
    "String (Another fundamental need or aspiration the product fulfills, framed as the progress users are trying to make, e.g., 'To streamline collaborative project management and improve team productivity on complex initiatives.') atleast of 54 words"
    ]
    }
    ]
    },
    {
    "title": "Competitive Landscape (Product-Focused)",
    "completed": false,
    "summary": "string (Summary outlining the Primary Focus Product's main competitors and how it differentiates itself within its specific market, based on website info and supplemented by general knowledge where stated.) atleast of 54 words",
    "content": "string (3–4 sentences describing direct and indirect competitors, and the product's strategic positioning against them, emphasizing details from official sources where possible.) atleast of 54 words",
    "points": [
    {
    "main": "Key Direct Competitors",
    "subPoints": [
    "Competitor A: [Name]. String (Known for [Their main strength/focus area]. If competitor details are from general knowledge, state so. If from company website, cite that.) atleast of 54 words",
    "Competitor B: [Name]. String (Similar detailed description for another direct competitor and its known strengths.) atleast of 54 words"
    ]
    },
    {
    "main": "Indirect Competition & Alternative Solutions",
    "subPoints": [
    "String (Other ways users currently address the core problem the Primary Focus Product solves, e.g., 'Utilizing generic spreadsheet software for data analysis, which lacks specialized features but is widely accessible,' inferred from product descriptions or general market understanding.) atleast of 54 words",
    "String (Description of another alternative solution or type of indirect competitor, e.g., 'Developing custom in-house tools, which offer tailored functionality but require significant development resources and ongoing maintenance.') atleast of 54 words"
    ]
    },
    {
    "main": "Positioning Against Competitors",
    "subPoints": [
    "String (How the product aims to win against direct competitors, e.g., 'By offering a more intuitive user interface and significantly faster data processing speeds, as highlighted by its UVP and differentiators from the company website.') atleast of 54 words",
    "String (Its key competitive advantage in the current landscape, e.g., 'Its unique focus on seamless integration with the broader [Company Name] ecosystem provides a unified user experience not easily matched by standalone competitors.') atleast of 54 words"
    ]
    }
    ]
    },
    {
    "title": "SWOT Analysis",
    "completed": false,
    "summary": "string (Summary of the Primary Focus Product's internal strengths and weaknesses, and the external opportunities and threats it faces, based on website information and general market knowledge.) atleast of 54 words",
    "content": "string (3–4 sentences providing a balanced overview of the product's strategic position based on the SWOT factors, emphasizing details from official sources for S & W.) atleast of 54 words",
    "points": [
    {
    "main": "Strengths",
    "subPoints": [
    "String (A key internal advantage, e.g., 'Leverages [Company Name]'s strong brand reputation and existing enterprise customer base for market penetration,' derived from website and JD analysis.) atleast of 54 words",
    "String (Another core competency, e.g., 'Possesses proprietary algorithms for [specific function] that deliver demonstrably superior accuracy compared to alternatives, as evidenced by case studies on the company website.') atleast of 54 words"
    ]
    },
    {
    "main": "Weaknesses",
    "subPoints": [
    "String (An internal limitation, e.g., 'The product currently has a steeper learning curve for non-technical users, potentially hindering wider adoption in certain segments,' inferred cautiously from website or JD.) atleast of 54 words",
    "String (Another area for improvement, e.g., 'Perceived as having a higher price point compared to some newer, more narrowly focused competitors, which could be a barrier for smaller businesses.') atleast of 54 words"
    ]
    },
    {
    "main": "Opportunities",
    "subPoints": [
    "String (A significant external market opportunity, e.g., 'The rapidly growing market demand for AI-powered automation in [target industry] presents a significant expansion opportunity for the product’s advanced capabilities.') atleast of 54 words",
    "String (Another potential opportunity, e.g., 'The increasing need for robust data privacy and compliance features offers a chance to further differentiate by enhancing its existing security architecture.') atleast of 54 words"
    ]
    },
    {
    "main": "Threats",
    "subPoints": [
    "String (A key external threat, e.g., 'Intense competition from both established players and agile startups introducing innovative features at a rapid pace, requiring continuous product development.') atleast of 54 words",
    "String (Another potential challenge, e.g., 'Potential shifts in technology standards or user preferences towards open-source alternatives could impact long-term market share if not proactively addressed.') atleast of 54 words"
    ]
    }
    ]
    }
    ]
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

    Points:

        mainPoint: Primary Mission / Underlying Need

            subPoints: Based on the responsibilities and objectives listed, articulate the fundamental problem this role is hired to solve for the company or product team. Explain the significance of this mission and why it's likely a priority now, drawing inferences from the JD text and **Do not add any Asterisk symbol anywhere**.

        mainPoint: Key Responsibility Areas & PM Activities

            subPoints: Break down the main tasks mentioned in the JD into logical groupings (e.g., Product Strategy, Execution, GTM, Analysis). For each, explain what the JD says is required and why it's important for this specific role. Connect responsibilities to typical PM functions and translate jargon into actionable terms (e.g., "owning the roadmap" likely means defining priorities and communicating trade-offs) and **Do not add any Asterisk symbol anywhere**.

        mainPoint: Areas of Specific Emphasis or Complexity

            subPoints: Identify any responsibility or task mentioned multiple times, listed first, or given particular detail/weight in the JD. Analyze why this area is likely a key focus for the hiring manager and what inherent complexities or challenges it might involve based on the JD's description **Do not add any Asterisk symbol anywhere**.

Card 2: Required Skills & Experience

    Title: Required Skills & Experience

    Summary: Interpretation of the essential and preferred qualifications sought, explaining their relevance to the role's demands.

    Points:

        mainPoint: Essential Hard Skills / Technical Requirements

            subPoints: List specific technical skills, tools, methodologies, or domain knowledge explicitly required. If none are specific, state this clearly ("Specific required technical skills not listed"). For each required skill, explain how it directly applies to fulfilling the responsibilities listed in Card 1 and why it's critical for success in this specific role based on the JD and *Do not add any Asterisk symbol anywhere*.

        mainPoint: Critical Soft Skills & Attributes

            subPoints: List essential communication, collaboration, leadership, or other behavioral attributes mentioned. Analyze why these specific soft skills are crucial for success, connecting them to the team structure (Card 4), stakeholder interactions, or challenges implied by the JD and *Do not add any Asterisk symbol anywhere*.

        mainPoint: Required Experience Level & Domain

            subPoints: Specify the minimum years of experience, industry domain, or functional experience requested. Analyze what this requirement suggests about the expected level of autonomy, complexity, or specific challenges the candidate will need to handle.

        mainPoint: Preferred / Standout Qualifications

            subPoints: List any 'nice-to-have' qualifications. Analyze what these preferred items reveal about the ideal candidate profile, potential future needs of the team/role, or areas where a candidate could truly differentiate themselves.

Card 3: Defining Success & Measuring Impact

    Title: Defining Success & Measuring Impact

    Summary: Analysis of how performance will be measured and the expected tangible outcomes of the role, based on explicit and inferred JD points.

    Points:

        mainPoint: Explicitly Stated Success Metrics / KPIs

            subPoints: List any specific metrics, goals, or KPIs mentioned in the JD (e.g., "increase user engagement," "achieve revenue target," "deliver on time"). Clearly state if "Specific metrics/KPIs not explicitly listed." For any metrics found, explain how successful execution of the responsibilities listed in Card 1 would directly influence these metrics.

        mainPoint: Implied Success Indicators

            subPoints: Based on the responsibilities, objectives, and desired outcomes described, infer other ways performance will likely be judged, even without explicit metrics (e.g., quality of strategic input, effectiveness of collaboration, user satisfaction outcomes, successful feature adoption). Explain the reasoning for each inference drawn from the JD text.

        mainPoint: Expected Business / Product Impact

            subPoints: Synthesize the desired tangible outcomes of the role's success for the product, team, or the business as a whole, based on statements in the JD (e.g., market share growth, operational efficiency, user base expansion). Explain the significance of this impact from a strategic perspective.

        mainPoint: Connecting Success to Interview Examples

            subPoints: Based on the metrics, implied indicators, and expected impact, suggest the types of interview examples (using STAR method or similar) the candidate should prepare to demonstrate their ability to achieve these specific outcomes or deliver this kind of impact.

Card 4: Team, Collaboration & Reporting Structure

    Title: Team, Collaboration & Reporting Structure

    Summary: Analysis of the organizational context, including reporting lines, key partners, and the expected style and challenges of collaboration.

    Points:

        mainPoint: Reporting Structure

            subPoints: State who the role reports to, if specified. Clearly state if "Reporting structure not specified in JD." Analyze what this reporting line might mean for the role's level of autonomy, strategic alignment, and typical interactions (e.g., reporting to a Director might mean less day-to-day guidance, reporting to a Senior PM might imply mentorship) and *Do not add any Asterisk symbol anywhere*.

        mainPoint: Key Internal Collaborators / Stakeholders

            subPoints: List specific internal teams or roles mentioned as partners (e.g., Engineering, Design, Marketing, Sales). For each, explain the nature of the collaboration implied by the JD's description of tasks (e.g., "collaborate closely with Engineering on technical feasibility and execution," "work with Marketing on GTM strategy and messaging") and *Do not add any Asterisk symbol anywhere*.

        mainPoint: Key External Collaborators / Relationships

            subPoints: List any external groups mentioned (e.g., customers, partners, suppliers). Explain the purpose and type of interaction with these external parties based on the JD. State if "Key external collaborators not specified in JD." and and *Do not add any Asterisk symbol anywhere*.

        mainPoint: Implied Collaboration Style & Potential Challenges

            subPoints: Analyze the JD text for clues about the required collaboration style (e.g., highly cross-functional, consensus-driven, requiring significant influence without direct authority, global/distributed). Based on the number and type of collaborators, point out any potential challenges in managing dependencies, competing priorities, or communication that are suggested by the structure and *Do not add any Asterisk symbol anywhere*.

Card 5: Strategic Context & Role Significance

    Title: Strategic Context & Role Significance

    Summary: Places the role within the broader company and product strategy, interpreting why this position is important now and its potential impact.

    Points:

        mainPoint: The Company's Need for this Role

            subPoints: Synthesize why the company is hiring for this position specifically at this time, based on the problems the role is intended to solve or the initiatives it supports (Card 1 analysis). Explain what strategic gap or opportunity the role is designed to address according to the JD. and *Do not add any Asterisk symbol anywhere*

        mainPoint: Contribution to Broader Product / Company Strategy

            subPoints: Explain how successful execution of this role's responsibilities directly contributes to the company's overall product vision, business objectives, or strategic priorities mentioned or implied in the JD. Connect the specific tasks to the bigger picture. and *Do not add any Asterisk symbol anywhere*

        mainPoint: Potential Strategic Challenges or Opportunities

            subPoints: Identify any strategic challenges (e.g., competitive intensity, market maturity, technological shifts) or significant opportunities (e.g., untapped market segment, new platform adoption) that the role is intended to navigate, address, or capitalize on, as suggested by the JD. and *Do not add any Asterisk symbol anywhere*

        mainPoint: Role Autonomy and Influence Level

            subPoints: Based on the responsibilities (Card 1), required experience level (Card 2), reporting structure (Card 4), and strategic context, infer the expected level of autonomy the person in this role will have and their potential for influencing product decisions and cross-functional teams and *Do not add any Asterisk symbol anywhere*.

Card 6: Key Themes & Interview Angles

    Title: Key Themes & Interview Angles

    Summary: Synthesizes overarching themes from the JD and suggests areas to focus on during interview preparation and discussion.

    Points:

        mainPoint: Overarching Themes & Priorities

            subPoints: Identify 2-3 major themes that appear repeatedly or are given significant weight throughout the JD (e.g., "Execution Focus," "Customer Obsession," "Data-Driven Decision Making," "Cross-functional Leadership," "Innovation"). Explain how these themes are reflected across the responsibilities and requirements and *Do not add any Asterisk symbol anywhere*.

        mainPoint: Areas Likely to be Deeply Probed

            subPoints: Based on the required skills, areas of emphasis, and potential challenges identified in the previous cards, highlight specific topics or experiences the candidate should be prepared to discuss in detail. This is where the interviewer will likely probe for depth and *Do not add any Asterisk symbol anywhere*.

        mainPoint: How to Align Your Experience

            subPoints: Provide actionable guidance on how the candidate should frame their past experiences to align directly with the core requirements, skills, and strategic context identified in this analysis. Suggest focusing examples (e.g., using STAR) on the most emphasized responsibilities and demonstrating the required skills and impact and *Do not add any Asterisk symbol anywhere*.

        mainPoint: Insightful Questions to Ask

            subPoints: Generate 3-5 potential questions the candidate could ask their interviewers, derived directly from ambiguities, strategic points, potential challenges, or missing information identified during this JD analysis. Frame these as questions that show thoughtful engagement with the role and its context and *Do not add any Asterisk symbol anywhere*.
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
        "points": [
            {
            "main": "Primary Mission / Underlying Need",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Key Responsibility Areas & PM Activities",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Areas of Specific Emphasis or Complexity",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        },
        {
        "title": "Required Skills & Experience",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "Essential Hard Skills / Technical Requirements",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Critical Soft Skills & Attributes",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Required Experience Level & Domain",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
             {
            "main": "Preferred / Standout Qualifications",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        },
        {
        "title": "Defining Success & Measuring Impact",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "Explicitly Stated Success Metrics / KPIs",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Implied Success Indicators",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Expected Business / Product Impact",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Connecting Success to Interview Examples",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        },
        {
        "title": "Team, Collaboration & Reporting Structure",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "Reporting Structure",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Key Internal Collaborators / Stakeholders",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Key External Collaborators / Relationships",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Implied Collaboration Style & Potential Challenges",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        },
        {
        "title": "Strategic Context & Role Significance",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "The Company's Need for this Role",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Contribution to Broader Product / Company Strategy",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Potential Strategic Challenges or Opportunities",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Role Autonomy and Influence Level",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        },
         {
        "title": "Key Themes & Interview Angles",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "Overarching Themes & Priorities",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Areas Likely to be Deeply Probed",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "How to Align Your Experience",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Insightful Questions to Ask",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        }
    ]
    }

    ''')
    return job_description_analysis

def resume_experience_to_highlight_to_stand_out_fun(data):
    resume_experience_to_highlight_to_stand_out =  (f'''Analyse this entire {data}'''
                                
                                '''
    ----
   # **Resume Experience you can highlight to stand out - Module 4**

This is current module 7 but in the new system it will be module 4

**Module Explanation (What's in it for the user):**

This module helps you strategically prepare for your interviews by directly comparing this resume against the specific {Job Description}
 you're targeting. It analyzes both documents to give you actionable 
insights, ensuring you can confidently showcase your most relevant 
qualifications and proactively address any potential concerns.

Here's what you'll get:

1. Key Strengths & Alignment: Pinpoints the areas where your resume clearly demonstrates the skills
and experiences the job description is asking for. This helps you
identify your strongest talking points.
2. Potential Gaps & How to Address: Constructively highlights significant requirements from the job
description that might not be immediately obvious from your resume.
Importantly, it provides suggestions on how to frame your existing
experience, discuss transferable skills, or prepare specific answers to
bridge these perceived gaps during the interview.
3. Standout Experiences to Highlight: Goes beyond simple keyword matching to identify 2-4 specific accomplishments or experiences from *your* resume that are particularly compelling for *this* role. For each standout point, it explains *why* it's relevant to the JD and *why* emphasizing it will help you differentiate yourself from other candidates.

Essentially,
 this module transforms your resume and the JD into a personalized 
interview prep guide, focusing your efforts on what matters most to 
stand out as a strong fit.
    ----
    Give me response in this JSON format only:
    {
    "quick_summary": "Very long information description that summarizes all of these cards or sub modules",
    "sub_modules": [
        {
        "title": "Key Strengths & Alignment",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        },
        {
        "title": "Potential Gaps & How to Address",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        },
        {
        "title": "Standout Experiences to Highlight",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        }
        ]
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
recruiter screen objectives to generate a comprehensive guide for this
role candidate's first call with a recruiter. Focus on 
interpreting the JD in the context of this screening stage, predicting 
likely questions tailored to the JD, suggesting effective ways to 
approach answers, and providing insightful questions for the candidate 
to ask, all within a 4-card JSON structure.

**Constraints for JSON Output:**

- Generate **exactly 4** sub_modules (cards) as detailed below.
- Keep the content field empty ("") for all sub_modules.
- Use the provided JD text as a key source for tailoring typical recruiter
screen topics, predicting questions, and extracting quick facts. If
Resume is also provided as input, use it *only* for guidance in crafting the "Tell me about yourself" pitch (Card 2), *not* for tailoring other questions or facts derived *from the JD*.
- Maintain a clear Product Management candidate's perspective.
- For subPoints, include specific examples of *predicted questions*, *suggested strategies/talking points*, and *insightful questions to ask*.
- Clearly state when information for a specific quick fact (like salary range or location/remote status) is *not found* or is ambiguous in the provided JD.
- Ensure the complexity of questions and suggested answers is appropriate for an initial recruiter screening call (generally higher level than
technical/panel interviews).

*Module Title:* Recruiter Screen Prep

*Key Interview Prep Snapshot (Quick Summary)*

- **Instruction:** Generate a concise (3-4 sentence) quick summary for the quick_summary JSON field.
- **Content:** Briefly state the purpose of the recruiter screen (basic fit,
qualifications check, logistics) and how this module helps (call
objectives, quick facts, predicted questions, questions to ask).
Explicitly state that this preparation is tailored based on the provided JD (and Resume, if used).

*Card 1: Call Rubric & Quick Facts*

- **Instruction:** Generate the JSON object for the first sub_module.
- *Title:* Call Rubric & Quick Facts
- *Summary Preview:* What the recruiter is screening for in this round and key logistical details from the JD.
- *Expanded Details:* (These become the mainPoints in the JSON points array)
    - Purpose of the Recruiter Screen: [Explain the main objectives from the
    recruiter's perspective (e.g., verify basic qualifications match JD,
    assess communication skills, gauge enthusiasm/fit signals, confirm
    logistics). Interpret *how* the recruiter will likely evaluate the candidate at this stage based on typical practices.]
    - Key Evaluation Areas: [Summarize the core things the recruiter will likely
    be listening for (e.g., clarity in communication, relevant experience
    keywords aligning with JD, demonstrated interest, alignment on key
    requirements like location/salary, basic cultural fit signals).]
    - Salary Information from JD: [State explicitly if a salary range or specific
    salary information was provided in the JD. If yes, state the
    information. If no, state "Salary information not provided in the JD."]
    - Location & Remote Status from JD: [State explicitly what the JD says about
    location requirements or remote work options. If it's ambiguous or not
    mentioned, state this clearly ("Location/remote status unclear from JD"
    or "Not specified in JD").]
    - Other Logistical Details in JD: [Mention any other logistical requirements
    explicitly stated (e.g., travel requirement, specific certification
    needed for legal/compliance reasons mentioned in JD). State if none
    specified.]

---

*Card 2: Craft Your Introduction*

- **Instruction:** Generate the JSON object for the second sub_module.
- *Title:* Craft Your Introduction
- *Summary Preview:* Guidance on creating a compelling "Tell me about yourself" pitch tailored to this specific role.
- *Expanded Details:* (These become the mainPoints)
    - Strategy for Tailoring Your Pitch: [Explain the importance of tailoring the
    "Tell me about yourself" answer to the specific JD. Advise connecting
    past experience directly to the required skills and responsibilities
    mentioned in the JD (reference key areas from JD analysis if available,
    otherwise infer from typical PM responsibilities). Explain the
    'Past-Present-Future' framework commonly used.]
    - Key Elements to Highlight (Based on JD): [Suggest specific types of
    experiences or skills from a typical PM background (or the candidate's
    resume if provided) that are most relevant to *this specific role* based on keywords, responsibilities, and required qualifications in the JD. Provide examples like "Highlight experience managing [type of
    project from JD]," "Emphasize your skills in [specific required skill
    from JD]."]
    - Connecting Your Experience to the Role's Needs: [Advise using language from the
    JD. For instance, if the JD emphasizes "cross-functional collaboration," suggest framing experiences using similar terms. If it mentions
    "driving impact," suggest concluding points by summarizing the positive
    outcomes of past work.]
    - Practice and Timing: [Advise practicing the pitch to be concise, ideally 2-3
    minutes long, focusing on clarity and enthusiasm, not rushing through
    details.]

---

*Card 3: Predicted Recruiter Questions*

- **Instruction:** Generate the JSON object for the third sub_module.
- *Title:* Predicted Recruiter Questions
- *Summary Preview:* Likely questions you'll be asked, tailored based on the JD and common screening topics.
- *Expanded Details:* (These become the mainPoints, each containing tailored question examples as subPoints)
    - Background and Experience Questions: [Generate 5-6 questions. Tailor these
    questions to probe the candidate's relevant past roles, industry
    experience (if specified or preferred in JD), and how their overall
    background aligns with the basic qualifications listed in the JD.]
    - Role-Specific & Foundational PM Questions: [Generate 4-5 questions. Tailor these
    questions to touch upon the key responsibilities, specific required
    skills/tools/methodologies, and domain expertise mentioned in the JD
    (linking to key areas from JD analysis if available). Keep these at a
    recruiter-level (higher level) check, not deep technical dives.]
    - Teamwork & Collaboration Questions: [Generate 4-5 questions. Tailor these
    questions based on the team structure, reporting lines, and implied
    collaboration style described in the JD (linking to key areas from JD
    analysis if available). Focus on how the candidate interacts with
    others.]
    - Motivation & Company/Product Interest Questions: [Generate 4-5 questions.
    Tailor these questions to ask about the candidate's specific interest in this role, the company, its products, and how their career goals align
    (linking to key areas from JD analysis if available).]
    - General & Logistical Questions: [Generate 3-5 questions. Include standard
    logistical questions not covered in Card 1 (e.g., "What are you looking
    for in terms of company culture?") and wrap up any other general
    questions relevant for screening.]

---

*Card 4: Insightful Questions to Ask*

- **Instruction:** Generate the JSON object for the fourth sub_module.
- *Title:* Insightful Questions to Ask
- *Summary Preview:* Recommended questions to ask the recruiter, tailored to the JD, to show engagement and gather information.
- *Expanded Details:* (These become the mainPoints, each containing tailored question examples as subPoints)
    - Questions About the Role & Team: [Generate 3-4 thoughtful questions about the day-to-day of the role, immediate priorities, team dynamics, or
    specific responsibilities mentioned in the JD that could use
    clarification. Frame these as questions a recruiter *can* likely answer and that show the candidate has thought about the role.]
    - Questions About the Interview Process: [Generate 2-3 essential questions about
    the next steps, number of rounds, timeline, and what the candidate
    should expect in subsequent interviews.]
    - Questions About Company/Team Culture from Recruiter's View: [Generate 2-3
    questions that leverage the recruiter's perspective on the company or
    product team culture, work environment, or values. Tailor if the JD
    hints at a specific culture or way of working (e.g., asking about
    collaboration style if the JD emphasizes it).]
    - Clarifying JD Details or Strategic Context: [Generate 1-2 questions specifically
    designed to clarify something potentially ambiguous or strategic
    mentioned in the JD (linking to key areas from JD analysis if
    available). Frame these as questions stemming from the candidate's
    analysis of the role.]

    ----
    Give me response in this JSON format only:
    {
    "quick_summary": "Very long information description that summarizes all of these cards or sub modules",
    "sub_modules": [
        {
        "title": "Call Rubric & Quick Facts",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        },
        {
        "title": "Craft Your Introduction",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        },
        {
        "title": "Predicted Recruiter Questions",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            
            "..."
        ]
        },
         {
        "title": "Insightful Questions to Ask",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            
            "..."
        ]
        }
        ]
        }
    ]
    }

    ''')
    return recruiter_screen_preparation

def favorite_product_question_fun(data):
    favorite_product_question =  (f'''Analyse this entire {data}'''
                                
                                '''
    ----
   Card 1: What’s Your Favorite Product?
    - title: "🧠 How to Answer Favorite Product Question"
    - summary: "A breakdown of one of the most common product management interview questions, why it’s asked, what to expect, variations, and how to answer effectively."
    - details (Map to 'points' array using 'main'/'subPoints'):
        - main: "🤔 Why Do Interviewers Ask This?", subPoints: [
            "This question acts as a low-pressure warm-up to help the interviewer evaluate:",
            "Your product thinking and user empathy",
            "Your ability to analyze strengths, weaknesses, and tradeoffs",
            "Your communication skills and enthusiasm for product work",
            "It’s also a fun way for them to get to know your interests and how you see the world."
        ]
        - main: "📋 What to Expect", subPoints: [
            "This is often the first real question in a PM interview.",
            "The conversation usually lasts 5–10 minutes.",
            "Expect a casual tone, but be ready for deeper follow-ups.",
            "Common follow-up questions include:",
            "How would you improve it?",
            "What’s a product you dislike?",
            "How would you measure its success?",
            "What if you were the CEO — what would you change?"
        ]
        - main: "🔁 Common Variants", subPoints: [
            "Interviewers may tweak the question to test your flexibility. Examples include:",
            "What’s your favorite Google product?",
            "What’s your favorite non-tech product?",
            "What are your top 3 favorite products?",
            "What’s a product you hate that others love?",
            "What’s a product with untapped potential?"
        ]
        - main: "💡 How to Choose a Good Product", subPoints: [
            "Pick something that reflects your:",
            "Passion — You enjoy using it and have real opinions about it.",
            "Perspective — You understand its strengths and limitations.",
            "Personality — It gives insight into how you think and work.",
            "Tips:",
            "✅ You can choose something popular — just add depth to your take.",
            "✅ Obscure products are fine — explain them clearly.",
            "❌ Avoid direct competitors of the company you’re interviewing with.",
            "❌ Avoid products that are too simple to discuss for 5–10 minutes."
        ]
        - main: "✏️ Example Product Improvement", subPoints: [
            "> “One thing I’d improve about Notion is its search experience. Right now, it’s hard to retrieve notes across pages. I’d introduce a lightweight tagging system, like #econ or #design, that automatically groups tagged content into a dynamic dashboard for easier synthesis.”"
        ]
---
Card 2: Favorite Product Answer Framework
    - title: "📘 Title: 5 Steps Framework"
    - summary: "Learn a proven 5-step framework to confidently answer the PM interview question: 'What is your favorite product and how would you improve it?'"
    - details (Map to 'points' array using 'main'/'subPoints'):

        - main: "✅ 1. Pick the Right Product", subPoints: [
            "Choose 3 digital and 1 physical product in advance",
            "Avoid:",
            "Culturally niche tools (e.g., WeChat, rice cookers)",
            "Overused answers (e.g., Spotify, Netflix)",
            "Select products your interviewer likely uses or knows"
        ]
        - main: "🧭 2. Intro in One Sentence", subPoints: [
            "Briefly describe what the product does.",
            "Example:",
            "“Waze helps users navigate from point A to B using real-time traffic data.”"
        ]
        - main: "👥 3. Define Customer Segments", subPoints: [
            "List 3–4 user types and highlight which one you identify with.",
            "Example:",
            "“As a new parent, I use Waze to avoid long drives with a crying baby.”"
        ]
        - main: "💢 4. Pain-Driven Features", subPoints: [
            "For each of 3 pain points, follow this formula:",
            "Pain → App Feature → Outcome",
            "Tie real, emotional user needs to key features",
            "Example:",
            "“Pain: Traffic stresses me out with kids in the car",
            "Feature: Waze reroutes in real time",
            "Outcome: I stay calm and get there faster.”"
        ]
        - main: "🔧 5. Suggest Improvements", subPoints: [
            "Use one or more of these 4 angles:",
            "1. 🎯 Align with the company’s mission",
            "2. 🚫 Address unmet user needs",
            "3. 🤖 Add tech-based value (e.g., AI-powered suggestions)",
            "4. 🎧 Improve the end-to-end journey (e.g., music/podcast integrations)"
        ]



    ----
    Give me response in this JSON format only:
    {
    "quick_summary": "Very long information description that summarizes all of these cards or sub modules",
    "sub_modules": [
        {
        "title": "What’s Your Favorite Product?",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "Summary",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Why Do Interviewers Ask This?",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "What to Expect",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Common Variants",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "How to Choose a Good Product",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Example Product Improvement",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        },
        {
        "title": "5 Steps Framework",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "Summary",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "1. Pick the Right Product",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "2. Intro in One Sentence",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "3. Define Customer Segments",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "4. Pain-Driven Features",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "5. Suggest Improvements",
            "subPoints": ["information description 1", "information description 2", "..."]
            }
            "..."
        ]
        }
    ]
    }

    ''')
    return favorite_product_question

def product_design_fun(data):
    product_design =  (f'''Analyse this entire {data}'''
                                
                                '''
    ----
   **Quick Summary**

Please provide a summary of the key learnings from [card 1] [card 2]

---

**Card 1: Overview of Product Design Questions**

**Summary**

Please provide a quick summary of the key learnings from the product design overview.

*Key Points* 

**What to Expect:**
*Describe the typical format of a product design question (e.g., open-ended, problem-solving).
*   List common types of product design questions (e.g., "Design X for Y," "Improve Z," "How would you measure success for W?").
*   Explain the general flow you should follow when answering (mentioning a process like the one we discussed previously, e.g., Clarify, User, Pain Points, Solution, Metrics).

**What Interviewers are Looking For:**

- Explain the core skills and mindsets that interviewers assess through these questions (e.g., Product Sense, User Empathy, Structured Thinking, Problem Solving, Creativity, Communication, Prioritization, Technical Feasibility awareness).
- Describe *how* they look for these qualities during your answer (e.g., through your clarifying questions, your user analysis, the structure of your response, the range of solutions considered, how you justify your choices).

**Sample Answers: "Good" vs. "Great":**

- Choose a single, representative sample product design question (e.g., "Design a product to help people find a hiking trail").
- Provide a "Good" answer to this question. This answer should follow a basic structure but might lack depth, strong rationale, or clear prioritization.
- Provide a "Great" answer to the *same* question. This answer should follow a structured framework rigorously, demonstrate deeper user understanding, stronger rationale for choices, consideration of trade-offs, clearer prioritization, and better communication.
- *Crucially*, provide a clear explanation highlighting the specific differences between the "Good" and the "Great" answer, pointing out *why* the "Great" answer is superior based on the criteria mentioned in the "What Interviewers are Looking For" section.

**Why do companies ask Product Design questions:**

- Explain the purpose of these questions from the company's perspective. Why is this a necessary part of the interview process? (e.g., To simulate real-world problem-solving, assess how candidates think under pressure, see their structured approach, evaluate communication skills, gauge passion for product).Provide any short historical context for such interview question.

**Evaluation Rubric:**

- Outline a hypothetical rubric that interviewers might use to evaluate candidates' answers.
- Break down the evaluation into key criteria (similar to the skills mentioned in section 2, e.g., Problem Framing, User Focus, Solutioning, Communication, Structure).
- For each criterion, briefly describe what different performance levels might look like (e.g., Poor, Good, Great, or similar levels). Provide tangible examples of what demonstrates "Good" vs. "Great" performance for each criterion *within the context of answering a product design question*.

---

**Card 2: How to Answer Product Design Questions**

- Sample LLM response
    
    ![Screen Shot 2025-05-05 at 2.31.44 AM.png](attachment:b212eadf-ffb9-44c1-a3fe-980e47889b5a:Screen_Shot_2025-05-05_at_2.31.44_AM.png)
    

**Summary**

Please provide a summary of the key learnings from the product design framework for answering product design questions

**Optional Instructions**

Act as an instructor explaining "Card 2: How to Answer Product Design Questions".

Teach me the step-by-step framework provided below. For EACH step in the framework, please include the specific examples, advice, rationale, frameworks, and sound bites mentioned in the list under that step.

Explain each step clearly before moving to the next, providing the requested details for each.

**Key points** 

Framework:

- Clarify and Get Context
    - (Include sample clarifying questions)
- Mission/Vision
    - (Include advice for known company mission)
    - (Include advice for unknown company mission)
- Define Personas (user groups)
    - (Include an example of user groups)
    - (Include advice on identifying groups)
    - (Include an example of prioritization rationale)
    - (Include advice on prioritizing groups)
- User Journey
    - (Include an example of a user journey)
    - (Include advice on articulating the journey)
- Identify User Pain Points and Opportunity Areas
    - (Include example/advice on finding pain points from journey)
    - (Include advice on prioritizing pain points for MVP)
- Brainstorm possible solutions
    - (Include advice on brainstorming a spectrum)
    - (Include advice on evaluating/prioritizing solutions for MVP)
- Define a product vision
    - (Include an example of a product/new feature vision)
- Prioritize features
    - (Include framework/advice on prioritizing features)
- Success Metrics
    - (Include sound bites/advice on defining success metrics)
- draft
    
    Summary
    
    Provide a summary of main takeaways for the product design questions framework below
    
    *Key Points* 
    
    Framework
    
    - Clarify and Get Context
        - provide sample clarifying questions
    - Mission/Vision
        - provide users advice on how to define the mission of the company if they know the company
        - provide users advice on how to define the mission of the company if they don’t know much about the company
    - Define Personas (user groups)
        - provide an example of defining user groups
        - provide advice on how to think through identifying the user groups
        - provide example of rationale on how to prioritize/choose a user group
        - provide advice on how to prioritize/choose a user group
    - User Journey
        - Provide an example of a user journey
        - Provide advice how to articulate user journey
    - Identify User Pain Points and Opportunity Areas
        - Provide example/advice on how to identify user pain points from the user journey
        - Provide advice on how prioritize pain points for the MVP
    - Brainstorm possible solutions
        - Provide advice on how to brainstorm a spectrum of solutions for the problem
        - Provide advice on how to evaluate prioritize solution (e.g., mission/vision, impact metrics)for the MVP
    - Define a product vision
        - Provide an example of a product/new feature vision
    - Prioritize features
        - Provide framework/advice on how to priortize features (e.g., pros/cons)
    - Success Metrics
        - Provide sound bites on how to define success metric for this new feature/product design
        

---

**Card 3: Sample product design question for [company]**

Based on the [job description] create a mock product design interview question that would be suitable for a candidate applying for this role.

**Card 4: Sample product design question for [company]**

Create a mock product design interview question that would be suitable for a candidate applying for this role focused on the industry based on the [company].

or 

Generate ONE open-ended product design question that:

1. Is highly relevant to the **[Industry Name] industry**.
2. Connects meaningfully to **[Company]** context (even if not directly about their most famous product feature).
3. Aligns with the **focus area, key responsibilities, and target user group** mentioned in the job description context.
4. Requires the candidate to think through a standard product design process (understanding users/problems, brainstorming solutions, considering trade-offs/feasibility, defining success metrics).

    ----
    Give me response in this JSON format only and ensure do not use any *asterisk* symbols anywhere:
    {
    "quick_summary": "Very long information description that summarizes all of these cards or sub modules",
    "sub_modules": [
        {
        "title": "Overview of Product Design Questions",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "What to Expect",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "What Interviewers are Looking For",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Sample Answers: "Good" vs. "Great"",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Why do companies ask Product Design questions",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Evaluation Rubric",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            "..."
        ]
        },
        {
        "title": "How to Answer Product Design Questions",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "Clarify and Get Context",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Mission/Vision",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Define Personas (user groups)",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "User Journey",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Identify User Pain Points and Opportunity Areas",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Brainstorm possible solutions",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Define a product vision",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Prioritize features",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "Success Metrics",
            "subPoints": ["information description 1", "information description 2", "..."]
            }
            "..."
        ]
        },
        {
        "title": "Sample product design question for [company]",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            
            "..."
        ]
        },
         {
        "title": "..",
"completed":false,
        "summary": "a full summary text of some long length that summarizes all these modules",
        "content": "some full long information text",
        "points": [
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            {
            "main": "some main title",
            "subPoints": ["information description 1", "information description 2", "..."]
            },
            
            "..."
        ]
        }
        ]
        }
    ]
    }

    ''')
    return product_design