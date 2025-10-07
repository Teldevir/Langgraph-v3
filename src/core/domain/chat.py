from typing import Annotated, TypedDict, Any
from langchain_ollama import ChatOllama
from langgraph.constants import START, END
from langgraph.graph import StateGraph, add_messages
from langgraph.graph.state import CompiledStateGraph

from src.core.data.db.postgres.memory import get_checkpointer
from src.core.domain.document_service import DocumentService
from src.config import SettingsSingleton, Settings


def get_llm() -> ChatOllama:
    settings: Settings = SettingsSingleton.get_instance()
    return ChatOllama(
        model=settings.langgraph.language_model,
        temperature=settings.langgraph.temperature,
    )


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State) -> State:
    llm: ChatOllama = get_llm()
    return {'messages': [llm.invoke(state['messages'])]}

def build_graph(checkpointer) -> CompiledStateGraph:
    graph_builder = StateGraph(State)
    graph_builder.add_node('chatbot', chatbot)
    graph_builder.add_edge(START, 'chatbot'),
    graph_builder.add_edge('chatbot', END),
    graph = graph_builder.compile(checkpointer=checkpointer)
    return graph

def ask(question: str, thread_id: str) -> str:
    with get_checkpointer() as checkpointer:
        checkpointer.setup()
        settings: Settings = SettingsSingleton.get_instance()
        base_prompt = settings.app.prompt
        graph: CompiledStateGraph = build_graph(checkpointer)
        service = DocumentService()
        context: str = service.search_with_formatting(question)

        prompt: str = f'{base_prompt}\nконтекст: {context}\nвопрос: {question}'
        user_input: State = {'messages': [{'role': 'user', 'content': prompt}]}
        config: dict[str, Any] = {'configurable': {'thread_id': thread_id}}
        state: State = graph.invoke(user_input, config=config)
        return state['messages'][-1].content

