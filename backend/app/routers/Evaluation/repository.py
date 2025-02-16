from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .models import Evaluation


async def get_evaluation_from_db(evaluation_id: str, sessionDB: AsyncSession) -> Evaluation | None:
    result = await sessionDB.execute(
        select(Evaluation).where(Evaluation.evaluation_id == evaluation_id)
    )
    return result.scalar_one_or_none()


async def create_evaluation_in_db(evaluation: Evaluation, sessionDB: AsyncSession) -> Evaluation:
    sessionDB.add(evaluation)
    await sessionDB.commit()
    await sessionDB.refresh(evaluation)
    return evaluation


async def update_evaluation_in_db(evaluation: Evaluation, sessionDB: AsyncSession) -> Evaluation:
    await sessionDB.execute(
        update(Evaluation)
        .where(Evaluation.evaluation_id == evaluation.evaluation_id)
        .values(evaluation.__dict__)
    )
    await sessionDB.commit()
    await sessionDB.refresh(evaluation)
    return evaluation


async def delete_evaluation_in_db(evaluation: Evaluation, sessionDB: AsyncSession) -> Evaluation:
    await sessionDB.delete(evaluation)
    await sessionDB.commit()
    return evaluation


async def get_evaluations_from_db(sessionDB: AsyncSession) -> list[Evaluation]:
    result = await sessionDB.execute(select(Evaluation))
    return result.scalars().all()
