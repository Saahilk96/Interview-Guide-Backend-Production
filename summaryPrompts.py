def generate_company_research_prompt(company_data):
    summary_prompt = f'''<role>
You are an expert interview preparation coach specializing in product manager interviews.
You have been given comprehensive company research data with multiple detailed modules.
Your task is to distill this into a focused, one-page executive summary.
</role>

<task>
Create a concise, one-page HTML summary containing ONLY the most critical information a product manager candidate needs for their interview.
Extract and synthesize the most important points from the provided company research data.
</task>

<input_data>
{company_data}
</input_data>

<selection_criteria>
Focus ONLY on information that:
1. Directly relates to product management roles and responsibilities
2. Will likely come up in interview conversations
3. Demonstrates candidate's research and preparation
4. Helps answer common interview questions about the company
5. Shows understanding of product strategy and market position
</selection_criteria>

<content_priorities>
Extract and include:
- Core business model and how they make money
- Main products (top 3–5 only) with one-line descriptions
- Target customers and their key problems
- What differentiates them from competitors
- Recent major developments (funding, launches, pivots)
- Current leadership (CEO and Head of Product only)
- One standout fact that shows deep research
</content_priorities>

<writing_style>
- Ultra-concise: every word must earn its place
- Action-oriented: focus on what the candidate can use
- Conversational but professional
- No fluff, jargon, or generic statements
- Write as if you have 2 minutes to brief someone
</writing_style>

<html_output_format>
IMPORTANT: Do NOT include <!DOCTYPE html>, <html>, <head>, or <body> tags.
Start directly with the content elements below.
Use only Tailwind CSS utility classes for styling.

<div class="px-6 py-4 space-y-6 text-sm bg-white text-gray-800">

  <h1 class="text-3xl font-bold text-gray-900 border-b-4 border-gray-300 pb-2">
    [Company Name] – PM Interview Brief
  </h1>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-gray-600 block mb-1">Founded</strong>
      [Year, founders if notable]
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-gray-600 block mb-1">Size & Status</strong>
      [Employees, Public/Private]
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-gray-600 block mb-1">Business Model</strong>
      [How they make money in one sentence]
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-gray-600 block mb-1">Target Market</strong>
      [Who they serve]
    </div>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      What They Build
    </h2>
    <div class="bg-gray-100 p-4 mt-2 rounded-md text-gray-800">
      [Top 3–5 products only, one line each, focused on user value]
    </div>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      Why They Win
    </h2>
    <p class="mt-2 text-gray-700 leading-relaxed">
      [2–3 sentences on their key differentiator and competitive advantage]
    </p>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      Recent Momentum
    </h2>
    <div class="border-l-4 border-gray-500 pl-4 mt-2 text-gray-700">
      [2–3 most significant recent developments that affect product strategy]
    </div>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      Leadership to Know
    </h2>
    <ul class="list-disc list-inside mt-2 space-y-1 text-gray-700">
      <li><strong>CEO:</strong> [Name and relevant background if notable]</li>
      <li><strong>Head of Product:</strong> [Name if available]</li>
    </ul>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      Your Interview Angle
    </h2>
    <p class="mt-2 text-gray-700 leading-relaxed">
      [2–3 sentences on what aspect of their business/product would be most interesting to discuss as a PM candidate]
    </p>
  </div>

</div>
</html_output_format>

<constraints>
- Maximum 500 words of actual content
- Must fit on one printed page
- Only include verified information from the source data
- If critical information is missing, omit the section rather than guess
- Focus on facts that demonstrate business acumen and product thinking
</constraints>'''

    return summary_prompt

def generate_product_research_prompt(product_data):
    product_prompt = f'''<role>
You are an expert interview preparation coach specializing in product manager interviews.
You have been given deep product research data for a company's flagship platform or service.
Your task is to distill this into a focused, one-page HTML product brief.
</role>

<task>
Create a concise, one-page HTML product summary focused on ONLY the most critical insights a PM candidate needs to understand the product deeply.
Extract, synthesize, and organize product-specific information to help the candidate demonstrate product thinking, strategic insight, and user empathy in the interview.
</task>

<input_data>
{product_data}
</input_data>

<selection_criteria>
Focus ONLY on information that:
1. Explains the product’s core value and functionality
2. Shows what differentiates it in the market
3. Demonstrates user understanding and key problems solved
4. Helps the candidate connect product vision with business outcomes
5. Equips the candidate to ask thoughtful product questions in the interview
</selection_criteria>

<content_priorities>
Extract and include:
- Product name and quick one-line description
- Target users and the main problem it solves for them
- Core features and how they deliver value
- Key differentiators vs competitors
- Underlying tech or ecosystem integrations (if relevant)
- Monetization model (if clear)
- One insight that reflects deep product understanding
- Strategic opportunity or product risk worth mentioning
</content_priorities>

<writing_style>
- Ultra-concise: think like a product one-pager
- PM-smart: highlight how and why decisions were likely made
- Conversational but sharp: professional, no buzzwords or filler
- Avoid speculation: only state what's supported by data
</writing_style>

<html_output_format>
IMPORTANT: Do NOT include <!DOCTYPE html>, <html>, <head>, or <body> tags.
Start directly with the content elements below.
Use only Tailwind CSS utility classes for styling.

<div class="px-6 py-4 space-y-6 text-sm bg-white text-gray-800">

  <h1 class="text-3xl font-bold text-gray-900 border-b-4 border-gray-300 pb-2">
    [Product Name] – PM Product Brief
  </h1>

  <div class="bg-gray-100 border-l-4 border-gray-500 p-4 rounded-md">
    <strong class="block font-semibold text-gray-600">Deep Insight:</strong>
    <span class="text-gray-800">[One key insight that reveals product strategy or tradeoff]</span>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-gray-600 block mb-1">Target Users</strong>
      <span class="text-gray-800">[Primary user personas and their pain points]</span>
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-gray-600 block mb-1">Core Problem Solved</strong>
      <span class="text-gray-800">[Main problem the product addresses]</span>
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-gray-600 block mb-1">Key Features</strong>
      <ul class="list-disc list-inside text-gray-700 mt-1 space-y-1">
        <li>[Feature 1 – user value]</li>
        <li>[Feature 2 – user value]</li>
        <li>[Feature 3 – user value]</li>
      </ul>
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-gray-600 block mb-1">Tech / Integrations</strong>
      <span class="text-gray-800">[Mention if the product leverages specific tech or ecosystems]</span>
    </div>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      Why It Wins
    </h2>
    <p class="mt-2 text-gray-700 leading-relaxed">
      [2–3 sentences on its unique value prop or strategic differentiators]
    </p>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      Business Model
    </h2>
    <p class="mt-2 text-gray-700 leading-relaxed">
      [Monetization strategy in one or two lines]
    </p>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      Strategy Watchpoint
    </h2>
    <div class="bg-gray-100 border-l-4 border-gray-500 p-4 mt-2 rounded-md">
      <span class="text-gray-800">[One strategic risk or opportunity for the product]</span>
    </div>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      Interview Angle
    </h2>
    <p class="mt-2 text-gray-700 leading-relaxed">
      [1–2 lines suggesting what an insightful PM candidate could ask or explore during the interview]
    </p>
  </div>

</div>
</html_output_format>

<constraints>
- Maximum 500 words of actual content
- Must fit on one printed page
- Only include verified information from the product data
- Leave out any sections if data is missing — do not guess
- Prioritize actionable insights over complete coverage
</constraints>'''

    return product_prompt
# def generate_recruiter_screen_preparation_prompt(recruiter_data):
#     prompt = f'''<role>
# You are an expert career coach specializing in helping candidates ace recruiter screening calls.
# You have been provided with detailed recruiter preparation data, including insights into the recruiter's goals, guidance for a self-introduction, and a list of questions to ask.
# Your task is to synthesize this information into a concise, actionable HTML summary designed to prepare a candidate for a recruiter screen.
# </role>

# <task>
# Create a concise, one-page HTML summary containing ONLY the most critical information a candidate needs to confidently navigate a recruiter screening call.
# Extract and synthesize the most important points from the provided recruiter preparation data.
# </task>

# <input_data>
# {recruiter_data}
# </input_data>

# <selection_criteria>
# Focus ONLY on information that:
# 1. Directly helps the candidate understand the recruiter's objectives.
# 2. Assists in crafting a compelling and tailored self-introduction.
# 3. Prepares the candidate for common recruiter questions.
# 4. Guides the candidate on what insightful questions to ask the recruiter.
# 5. Boosts clarity, confidence, and conversational readiness.
# </selection_criteria>

# <content_priorities>
# Extract and include:
# - The main purpose and evaluation areas of a recruiter screen.
# - Key logistical details from the JD (salary, location, remote status if available).
# - A strategic framework for the self-introduction (e.g., Past-Present-Future).
# - Key elements from the JD to highlight in the introduction.
# - Types of questions to ask the recruiter (about role, process, culture, JD clarifications).
# </content_priorities>

# <writing_style>
# - Ultra-concise: every word must earn its place.
# - Action-oriented: focus on what the candidate can immediately use.
# - Encouraging and confident tone.
# - No fluff, jargon, or generic statements.
# - Write as if you have 2 minutes to brief someone.
# </writing_style>

# <html_output_format>
# IMPORTANT: Do NOT include <!DOCTYPE html>, <html>, <head>, or <body> tags.
# Start directly with the content elements below.
# Use only Tailwind CSS utility classes for styling.

# <div class="px-6 py-4 space-y-6 text-sm">

#   <h1 class="text-3xl font-bold text-[#2c3e50] border-b-4 border-purple-500 pb-2">
#     Recruiter Screen Prep: Your Go-To Guide
#   </h1>

#   <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
#     <div class="bg-gray-100 p-4 rounded-lg">
#       <strong class="text-purple-500 block mb-1">Screen Purpose</strong>
#       [Purpose of the recruiter screen in one concise sentence, e.g., "Assess fit based on qualifications, communication, and logistics."]
#     </div>
#     <div class="bg-gray-100 p-4 rounded-lg">
#       <strong class="text-purple-500 block mb-1">Key Evaluation Areas</strong>
#       [Bulleted list of 2-3 key areas recruiters evaluate, e.g., "Skill/experience articulation, role interest, logistical alignment."]
#     </div>
#     <div class="bg-gray-100 p-4 rounded-lg">
#       <strong class="text-purple-500 block mb-1">JD Salary Info</strong>
#       [Salary information from JD, or "Not provided in JD."]
#     </div>
#     <div class="bg-gray-100 p-4 rounded-lg">
#       <strong class="text-purple-500 block mb-1">JD Location/Remote</strong>
#       [Location and remote status from JD, or "Unclear from JD."]
#     </div>
#   </div>

#   <div>
#     <h2 class="text-xl font-semibold text-[#34495e] mt-8 uppercase tracking-wider">
#       Craft Your Introduction
#     </h2>
#     <div class="bg-purple-100 p-4 mt-2 rounded-md text-gray-900">
#       <strong class="block mb-1 text-purple-700">Strategy:</strong> [Brief strategy for introduction, e.g., "Use Past-Present-Future, align with JD themes."]
#       <strong class="block mt-2 mb-1 text-purple-700">Highlight:</strong> [Bulleted list of 2-3 key elements to highlight based on JD, e.g., "Relevant project management, team collaboration."]
#       <strong class="block mt-2 mb-1 text-purple-700">Tip:</strong> [One concise tip, e.g., "Keep it 2-3 minutes, use JD keywords."]
#     </div>
#   </div>

#   <div>
#     <h2 class="text-xl font-semibold text-[#34495e] mt-8 uppercase tracking-wider">
#       Questions to Ask the Recruiter
#     </h2>
#     <ul class="list-disc list-inside mt-2 space-y-1 text-gray-800">
#       <li><strong>Role & Team:</strong> [1-2 example questions, e.g., "Immediate priorities for the role?", "Team structure?"]</li>
#       <li><strong>Interview Process:</strong> [1-2 example questions, e.g., "Next steps?", "Hiring timeline?"]</li>
#       <li><strong>Culture & Environment:</strong> [1-2 example questions, e.g., "Team culture?", "Traits of successful members?"]</li>
#       <li><strong>JD Clarification:</strong> [1 example question if applicable, e.g., "Clarify 'strategic impact' in JD?"]</li>
#     </ul>
#   </div>

#   <div>
#     <h2 class="text-xl font-semibold text-[#34495e] mt-8 uppercase tracking-wider">
#       Confidence Boosters
#     </h2>
#     <p class="mt-2 text-gray-800 leading-relaxed">
#       Remember: Your goal is to clearly articulate your fit, show enthusiasm, and confirm logistical alignment. Be yourself, be clear, and be confident!
#     </p>
#   </div>

# </div>
# </html_output_format>

# <constraints>
# - Maximum 400 words of actual content.
# - Must fit on one printed page.
# - Only include verified information from the source data.
# - If critical information is missing (e.g., salary), explicitly state "Not provided" or "Unclear" rather than omitting the section or guessing.
# - Focus on actionable advice for the candidate.
# </constraints>'''

#     return prompt

def generate_recruiter_screen_preparation_prompt(recruiter_data):
    prompt = f'''<role>
You are an expert career coach specializing in helping candidates ace recruiter screening calls.
You have been provided with detailed recruiter preparation data, including insights into the recruiter's goals, guidance for a self-introduction, and a list of questions to ask.
Your task is to synthesize this information into a concise, actionable HTML summary designed to prepare a candidate for a recruiter screen.
</role>

<task>
Create a concise, one-page HTML summary containing ONLY the most critical information a candidate needs to confidently navigate a recruiter screening call.
Extract and synthesize the most important points from the provided recruiter preparation data.
</task>

<input_data>
{recruiter_data}
</input_data>

<selection_criteria>
Focus ONLY on information that:
1. Directly helps the candidate understand the recruiter's objectives.
2. Assists in crafting a compelling and tailored self-introduction.
3. Prepares the candidate for common recruiter questions.
4. Guides the candidate on what insightful questions to ask the recruiter.
5. Boosts clarity, confidence, and conversational readiness.
</selection_criteria>

<content_priorities>
Extract and include:
- The main purpose and evaluation areas of a recruiter screen.
- Key logistical details from the JD (salary, location, remote status if available).
- A strategic framework for the self-introduction (e.g., Past-Present-Future).
- Key elements from the JD to highlight in the introduction.
- Types of questions to ask the recruiter (about role, process, culture, JD clarifications).
</content_priorities>

<writing_style>
- Ultra-concise: every word must earn its place.
- Action-oriented: focus on what the candidate can immediately use.
- Encouraging and confident tone.
- No fluff, jargon, or generic statements.
- Write as if you have 2 minutes to brief someone.
</writing_style>

<html_output_format>
IMPORTANT: Do NOT include <!DOCTYPE html>, <html>, <head>, or <body> tags.
Start directly with the content elements below.
Use only Tailwind CSS utility classes for styling.

<div class="px-6 py-4 space-y-6 text-sm bg-white text-gray-800">

  <h1 class="text-3xl font-bold text-gray-900 border-b-4 border-gray-300 pb-2">
    Recruiter Screen Prep: Your Go-To Guide
  </h1>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-gray-600 block mb-1">Screen Purpose</strong>
      <span class="text-gray-800">[Purpose of the recruiter screen in one concise sentence, e.g., "Assess fit based on qualifications, communication, and logistics."]</span>
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-gray-600 block mb-1">Key Evaluation Areas</strong>
      <ul class="list-disc list-inside text-gray-700 mt-1 space-y-1">
        <li>[Bulleted list of 2-3 key areas recruiters evaluate, e.g., "Skill/experience articulation, role interest, logistical alignment."]</li>
      </ul>
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-gray-600 block mb-1">JD Salary Info</strong>
      <span class="text-gray-800">[Salary information from JD, or "Not provided in JD."]</span>
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-gray-600 block mb-1">JD Location/Remote</strong>
      <span class="text-gray-800">[Location and remote status from JD, or "Unclear from JD."]</span>
    </div>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      Craft Your Introduction
    </h2>
    <div class="bg-gray-100 p-4 mt-2 rounded-md">
      <strong class="block mb-1 text-gray-600">Strategy:</strong>
      <span class="text-gray-800">[Brief strategy for introduction, e.g., "Use Past-Present-Future, align with JD themes."]</span>
      <strong class="block mt-2 mb-1 text-gray-600">Highlight:</strong>
      <ul class="list-disc list-inside text-gray-700 mt-1 space-y-1">
        <li>[Bulleted list of 2-3 key elements to highlight based on JD, e.g., "Relevant project management, team collaboration."]</li>
      </ul>
      <strong class="block mt-2 mb-1 text-gray-600">Tip:</strong>
      <span class="text-gray-800">[One concise tip, e.g., "Keep it 2-3 minutes, use JD keywords."]</span>
    </div>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      Questions to Ask the Recruiter
    </h2>
    <ul class="list-disc list-inside mt-2 space-y-1 text-gray-700">
      <li><strong>Role & Team:</strong> <span class="text-gray-800">[1-2 example questions, e.g., "Immediate priorities for the role?", "Team structure?"]</span></li>
      <li><strong>Interview Process:</strong> <span class="text-gray-800">[1-2 example questions, e.g., "Next steps?", "Hiring timeline?"]</span></li>
      <li><strong>Culture & Environment:</strong> <span class="text-gray-800">[1-2 example questions, e.g., "Team culture?", "Traits of successful members?"]</span></li>
      <li><strong>JD Clarification:</strong> <span class="text-gray-800">[1 example question if applicable, e.g., "Clarify 'strategic impact' in JD?"]</span></li>
    </ul>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-gray-900 mt-8 uppercase tracking-wider">
      Confidence Boosters
    </h2>
    <p class="mt-2 text-gray-700 leading-relaxed">
      Remember: Your goal is to clearly articulate your fit, show enthusiasm, and confirm logistical alignment. Be yourself, be clear, and be confident!
    </p>
  </div>

</div>
</html_output_format>

<constraints>
- Maximum 400 words of actual content.
- Must fit on one printed page.
- Only include verified information from the source data.
- If critical information is missing (e.g., salary), explicitly state "Not provided" or "Unclear" rather than omitting the section or guessing.
- Focus on actionable advice for the candidate.
</constraints>'''

    return prompt