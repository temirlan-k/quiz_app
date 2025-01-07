
from typing import List, Protocol
from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.models.question import Question,QuestionLocalization
from sqlalchemy.ext.asyncio import AsyncSession


class IQuestionRepository(Protocol):

    @abstractmethod
    async def get_by_id(self, id: UUID)-> Question | None: ...

    @abstractmethod
    async def create_question(self,)-> Question: ...

    @abstractmethod
    async def create_question_localization(self,)-> QuestionLocalization: ...
    

class QuestionRepository(IQuestionRepository):

    def __init__(self, session: AsyncSession)-> None:
        self.session = session
    
    async def get_by_id(self, id: UUID)-> Question | None:
        result = await self.session.get(Question,id)
        return result

    async def get_list_by_quiz_id(self,quiz_id:UUID,language)->List[QuestionLocalization]:
        result = await self.session.execute(
            select(QuestionLocalization)
            .join(Question, QuestionLocalization.question_id == Question.id)
            .where(Question.quiz_id == quiz_id)
            .where(QuestionLocalization.language == language)
            .options(joinedload(QuestionLocalization.question)) 
        )

        return result.scalars().all()


    async def create_question(self, attributes: dict)-> Question:
        question = Question(**attributes)
        self.session.add(question)
        await self.session.flush()
        return question
    
    async def create_question_localization(self,attributes: dict)-> QuestionLocalization:
        question_loc = QuestionLocalization(**attributes)
        self.session.add(question_loc)
        await self.session.flush()
        return question_loc
    

