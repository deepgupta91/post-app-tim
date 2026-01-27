from fastapi import FastAPI , HTTPException , File , UploadFile ,  Form , Depends
from app.schema import PostCreate, PostResponse, UserRead, UserCreate, UserUpdate
app = FastAPI()

from app.db import Post,create_db_and_tables ,get_async_session,User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select 

from app.images import imagekit

from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from app.users import auth_backend, current_active_user, fastapi_users


import shutil
import os
import uuid
import tempfile



@asynccontextmanager
async def lifespan(app : FastAPI):
    await create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan)


app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        caption: str = Form(""),
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )
        # print(upload_result)

        if upload_result.response_metadata.http_status_code == 200:
            post = Post(
                user_id=user.id,
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()



@app.get("/feed")
async def get_feed(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user),
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    user_dict = {u.id: u.email for u in users}

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
                "is_owner": post.user_id == user.id,
                "email": user_dict.get(post.user_id, "Unknown")
            }
        )

    return {"posts": posts_data}


@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user),):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="You don't have permission to delete this post")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 













# text_posts = {
#     1: {
#         "title": "Python Basics",
#         "content": "Python is a high-level, interpreted programming language known for its simplicity."
#     },
#     2: {
#         "title": "FastAPI Framework",
#         "content": "FastAPI is a modern web framework used to build high-performance REST APIs in Python."
#     },
#     3: {
#         "title": "Virtual Environment",
#         "content": "A virtual environment helps isolate project dependencies and avoid version conflicts."
#     },
#     4: {
#         "title": "Database Choice",
#         "content": "PostgreSQL is an advanced open-source relational database system."
#     },
#     5: {
#         "title": "ORM Concept",
#         "content": "SQLAlchemy allows developers to interact with databases using Python objects instead of SQL."
#     },
#     6: {
#         "title": "API Architecture",
#         "content": "REST APIs follow a stateless architecture and use HTTP methods like GET and POST."
#     },
#     7: {
#         "title": "Web Security",
#         "content": "HTTPS encrypts data between client and server, making communication secure."
#     },
#     8: {
#         "title": "Data Format",
#         "content": "JSON is a lightweight data interchange format commonly used in APIs."
#     },
#     9: {
#         "title": "Async Programming",
#         "content": "Async and await allow non-blocking execution, improving application performance."
#     },
#     10: {
#         "title": "Containerization",
#         "content": "Docker packages applications with their dependencies into portable containers."
#     },
#     11: {
#         "title": "Version Control",
#         "content": "Git helps track code changes, while GitHub is used for collaboration and hosting repositories."
#     },
#     12: {
#         "title": "System Design",
#         "content": "Microservices architecture breaks applications into small, independent services."
#     }
# }

# @app.get("/posts")
# def get_posts(limit : int = None):
#     if limit :
#         return list(text_posts.values())[:limit]
#     return text_posts

# @app.get("/posts/{id}")
# async def get_by_id(id : int):
#     if id not in text_posts:
#         raise HTTPException(status_code=404 , detail="data not found")
    
#     return text_posts.get(id)


# @app.post("/post")
# async def create_post(post : PostCreate):
#     text_posts[max(text_posts.keys())+1] = {"title" : post.title , "content" : post.content}
#     return post

# @app.delete('/delete/{id}')
# def delete_post(id : int):
#     if not id:
#         return {"please enter id to delete"}
#     return text_posts.pop(id)