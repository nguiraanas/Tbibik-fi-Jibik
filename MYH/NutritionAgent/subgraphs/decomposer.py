"""
Decomposer subgraph for semantic message analysis
"""

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langgraph.graph import StateGraph, START, END

from models.state_models import InquiryState
from config.llm_config import LLMConfig

class DecomposerSubgraph:
    """Handles semantic decomposition of user messages into TOON format"""
    
    def __init__(self):
        self.llm = LLMConfig.get_client("decomposer")
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the decomposer subgraph"""
        
        # System message for decomposer
        system_message = SystemMessage(
            content="""You are a Semantic Message Decomposer.

Your task: take **any user message** and break it into three categories:
1. **QUESTIONS** – anything the user is explicitly or implicitly asking.
2. **INFORMATION** – symptoms, facts, personal details, observations, statements.
3. **OUT_OF_CONTEXT** – jokes, random text, filler words, chit-chat, irrelevant content.

❗ Important rules:
- Work at the **sentence/semantic-unit** level.
- A message may produce **0, 1, 2 or 3 categories at once**.
- Extract **every distinct meaning**, even if short.
- Reformulate each extracted unit **clearly and concisely**.
- Do **not** answer questions, do **not** diagnose, do **not** give advice.
- Output **only TOON**, no commentary.

### Output Format
Return only this structure (TOON):

QUESTIONS:
- ...
- ...

INFORMATION:
- ...
- ...

OUT_OF_CONTEXT:
- ...
- ...

"""
        )
        
        # Few-shot examples
        few_shots_list = [
            {
                "human": "I feel tired lately and my waist increased by 2 cm. Should I worry or is it normal?",
                "assistant": """<TOON>
Questions:
• Should I worry?
• Is this normal?

Information:
• The user feels tired lately.
• The user's waist circumference increased by 2 cm.

Out_of_context:
• —
</TOON>"""
            },
            {
                "human": "ok lol btw I think my glucose is high after eating pasta?",
                "assistant": """<TOON>
Questions:
• Is my glucose high after eating pasta?

Information:
• The user believes their glucose rises after eating pasta.

Out_of_context:
• ok lol
• btw
</TOON>"""
            },
            {
                "human": "My sleep was bad lately, and my clothes feel tight. Also can you tell me what insulin resistance even means?",
                "assistant": """<TOON>
Questions:
• What does insulin resistance mean?

Information:
• The user reports poor sleep lately.
• The user's clothes feel tighter, suggesting possible body-size changes.

Out_of_context:
• —
</TOON>"""
            }
        ]
        
        few_shots_prompt = ChatPromptTemplate.from_messages([
            ("human", "{human}"),
            ("ai", "{assistant}")
        ])
        
        few_shots = FewShotChatMessagePromptTemplate(
            examples=few_shots_list,
            example_prompt=few_shots_prompt,
        )
        
        full_prompt = ChatPromptTemplate.from_messages([
            system_message,
            few_shots,
            ("human", "{input}"),
        ])
        
        self.chain = full_prompt | self.llm
        
        # Build graph
        builder = StateGraph(InquiryState)
        builder.add_node("decomposer", self._decompose_message)
        builder.add_edge(START, "decomposer")
        builder.add_edge("decomposer", END)
        
        return builder.compile()
    
    def _decompose_message(self, state: InquiryState) -> InquiryState:
        """Node function - processes input and returns TOON decomposition"""
        result = self.chain.invoke({"input": state["input"]})
        
        return {
            "messages": [result],
            "decompositions": state["decompositions"] + [result.content],
            "last_decomposition": result.content
        }
    
    def invoke(self, state: InquiryState) -> InquiryState:
        """Invoke the decomposer subgraph"""
        return self.graph.invoke(state)