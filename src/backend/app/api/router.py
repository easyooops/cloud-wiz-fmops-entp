from fastapi import APIRouter
from app.api.v1 import provider, inquiry, auth, agent, chain, chat, model, credential, store
from app.api.v1 import chat_model, embedding, vector_store, processing
from app.api.v1 import contactus, opinion

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"], prefix="/auth")
api_router.include_router(agent.router, tags=["agent"], prefix="/agent")
api_router.include_router(chain.router, tags=["chain"], prefix="/chain")
api_router.include_router(provider.router, tags=["provider"], prefix="/provider")
api_router.include_router(credential.router, tags=["credential"], prefix="/credential")
api_router.include_router(processing.router, tags=["processing"], prefix="/processing")
api_router.include_router(inquiry.router, tags=["inquiry"], prefix="/inquiry")
api_router.include_router(store.router, tags=["store"], prefix="/store")
api_router.include_router(chat.router, tags=["chat"], prefix="/chat")
api_router.include_router(chat_model.router, tags=["chat_model"], prefix="/chat_model")
api_router.include_router(model.router, tags=["model"], prefix="/model")
api_router.include_router(embedding.router, tags=["embedding"], prefix="/embedding")
api_router.include_router(vector_store.router, tags=["vector_store"], prefix="/vector_store")
api_router.include_router(contactus.router, tags=["contactus"], prefix="/contactus")
api_router.include_router(opinion.router, tags=["opinion"], prefix="/opinion")
