from fastapi import APIRouter
from app.api.v1 import provider, inquiry, auth, agent, credential, store
from app.api.v1 import processing
from app.api.v1 import contactus, opinion

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"], prefix="/auth")
api_router.include_router(agent.router, tags=["agent"], prefix="/agent")
api_router.include_router(provider.router, tags=["provider"], prefix="/provider")
api_router.include_router(credential.router, tags=["credential"], prefix="/credential")
api_router.include_router(processing.router, tags=["processing"], prefix="/processing")
api_router.include_router(inquiry.router, tags=["inquiry"], prefix="/inquiry")
api_router.include_router(store.router, tags=["store"], prefix="/store")
api_router.include_router(contactus.router, tags=["contactus"], prefix="/contactus")
api_router.include_router(opinion.router, tags=["opinion"], prefix="/opinion")
