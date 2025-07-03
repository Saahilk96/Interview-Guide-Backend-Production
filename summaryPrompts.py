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
<</input_data>

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

<div class="px-6 py-4 space-y-6 text-sm">

  <h1 class="text-3xl font-bold text-[#2c3e50] border-b-4 border-blue-500 pb-2">
    [Company Name] – PM Interview Brief
  </h1>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-blue-500 block mb-1">Founded</strong>
      [Year, founders if notable]
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-blue-500 block mb-1">Size & Status</strong>
      [Employees, Public/Private]
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-blue-500 block mb-1">Business Model</strong>
      [How they make money in one sentence]
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-blue-500 block mb-1">Target Market</strong>
      [Who they serve]
    </div>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-[#34495e] mt-8 uppercase tracking-wider">
      What They Build
    </h2>
    <div class="bg-blue-100 p-4 mt-2 rounded-md text-gray-900">
      [Top 3–5 products only, one line each, focused on user value]
    </div>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-[#34495e] mt-8 uppercase tracking-wider">
      Why They Win
    </h2>
    <p class="mt-2 text-gray-800 leading-relaxed">
      [2–3 sentences on their key differentiator and competitive advantage]
    </p>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-[#34495e] mt-8 uppercase tracking-wider">
      Recent Momentum
    </h2>
    <div class="border-l-4 border-green-600 pl-4 mt-2 text-gray-800">
      [2–3 most significant recent developments that affect product strategy]
    </div>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-[#34495e] mt-8 uppercase tracking-wider">
      Leadership to Know
    </h2>
    <ul class="list-disc list-inside mt-2 space-y-1 text-gray-800">
      <li><strong>CEO:</strong> [Name and relevant background if notable]</li>
      <li><strong>Head of Product:</strong> [Name if available]</li>
    </ul>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-[#34495e] mt-8 uppercase tracking-wider">
      Your Interview Angle
    </h2>
    <p class="mt-2 text-gray-800 leading-relaxed">
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
<</input_data>

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

<div class="px-6 py-4 space-y-6 text-sm">

  <h1 class="text-3xl font-bold text-[#2c3e50] border-b-4 border-indigo-500 pb-2">
    [Product Name] – PM Product Brief
  </h1>

  <div class="bg-indigo-100 border-l-4 border-indigo-400 p-4 rounded-md">
    <strong class="block font-semibold">Deep Insight:</strong>
    [One key insight that reveals product strategy or tradeoff]
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-indigo-500 block mb-1">Target Users</strong>
      [Primary user personas and their pain points]
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-indigo-500 block mb-1">Core Problem Solved</strong>
      [Main problem the product addresses]
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-indigo-500 block mb-1">Key Features</strong>
      <ul class="list-disc list-inside text-gray-800 mt-1 space-y-1">
        <li>[Feature 1 – user value]</li>
        <li>[Feature 2 – user value]</li>
        <li>[Feature 3 – user value]</li>
      </ul>
    </div>
    <div class="bg-gray-100 p-4 rounded-lg">
      <strong class="text-indigo-500 block mb-1">Tech / Integrations</strong>
      [Mention if the product leverages specific tech or ecosystems]
    </div>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-[#34495e] mt-8 uppercase tracking-wider">
      Why It Wins
    </h2>
    <p class="mt-2 text-gray-800 leading-relaxed">
      [2–3 sentences on its unique value prop or strategic differentiators]
    </p>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-[#34495e] mt-8 uppercase tracking-wider">
      Business Model
    </h2>
    <p class="mt-2 text-gray-800 leading-relaxed">
      [Monetization strategy in one or two lines]
    </p>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-[#34495e] mt-8 uppercase tracking-wider">
      Strategy Watchpoint
    </h2>
    <div class="bg-red-100 border-l-4 border-red-400 p-4 mt-2 rounded-md text-gray-800">
      [One strategic risk or opportunity for the product]
    </div>
  </div>

  <div>
    <h2 class="text-xl font-semibold text-[#34495e] mt-8 uppercase tracking-wider">
      Interview Angle
    </h2>
    <p class="mt-2 text-gray-800 leading-relaxed">
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
