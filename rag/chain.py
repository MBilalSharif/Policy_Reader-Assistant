from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs) 
def build_chain(retriever, prompt, model):
    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
    })

    parser = StrOutputParser()
    main_chain = parallel_chain | prompt | model | parser
    return main_chain