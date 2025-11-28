from typing import List, Optional

from src.modules.storage.models import File, Tag, FileTag
from src.modules.user.models import User
from sqlalchemy import select, func


class StorageRepository:
    def __init__(self, session):
        self.__session = session

    def create_file(self,
                    title: str,
                    file_path: str,
                    file_size: int,
                    file_type: str,
                    file_hash: str,
                    user_id: int,
                    category_id: int,
                    source_id: int,
                    first_lines: Optional[str] = None,
                    ) -> File:
        db_file = File(
            title=title,
            file_path=file_path,
            first_lines=first_lines,
            file_size=file_size,
            file_type=file_type,
            user_id=user_id,
            category_id=category_id,
            source_id=source_id,
            file_hash=file_hash,
        )

        self.__session.add(db_file)
        self.__session.commit()
        self.__session.refresh(db_file)
        return db_file

    def get_all_files(self) -> List[File]:
        stmt = select(File).order_by(File.last_modified)
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def get_all_files_paginated(self, skip: int = 0, limit: int = 100) -> List[File]:
        stmt = select(File).order_by(File.last_modified).offset(skip).limit(limit)
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def get_file_by_id(self, file_id: int) -> Optional[File]:
        stmt = select(File).where(File.id == file_id)
        res = self.__session.execute(stmt)
        return res.scalar_one_or_none()

    def get_files_by_user(self, user_id: int) -> List[File]:
        stmt = select(File).where(File.user_id == user_id).order_by(File.last_modified.desc())
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def get_files_by_user_paginated(self, user_id: int, skip: int = 0, limit: int = 100) -> List[File]:
        stmt = select(File).where(File.user_id == user_id).order_by(File.last_modified.desc()).offset(skip).limit(limit)
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def get_files_by_category(self, category_id: int) -> List[File]:
        stmt = select(File).where(File.category_id == category_id).order_by(File.last_modified.desc())
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def get_files_by_category_paginated(self, category_id: int, skip: int = 0, limit: int = 100) -> List[File]:
        stmt = select(File).where(File.category_id == category_id).order_by(File.last_modified.desc()).offset(
            skip).limit(limit)
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def get_files_by_tag_id(self, tag_id: int) -> List[File]:
        stmt = select(File).join(FileTag, File.id == FileTag.file_id).where(FileTag.tag_id == tag_id).order_by(
            File.last_modified.desc())
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def get_files_by_tag_id_paginated(self, tag_id: int, skip: int = 0, limit: int = 100) -> List[File]:
        stmt = select(File).join(FileTag, File.id == FileTag.file_id).where(FileTag.tag_id == tag_id).order_by(
            File.last_modified.desc()).offset(skip).limit(limit)
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def get_files_by_tag_id_list(self, tag_id_list: List[int]) -> List[File]:
        stmt = select(File).join(FileTag, File.id == FileTag.file_id).where(FileTag.tag_id.in_(tag_id_list)).order_by(
            File.last_modified.desc())
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def get_files_by_tag_id_list_paginated(self, tag_id_list: List[int], skip: int = 0, limit: int = 100) -> List[File]:
        stmt = select(File).join(FileTag, File.id == FileTag.file_id).where(FileTag.tag_id.in_(tag_id_list)).order_by(
            File.last_modified.desc()).offset(skip).limit(limit)
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def get_files_by_source(self, source_id: int) -> List[File]:
        stmt = select(File).where(File.source_id == source_id).order_by(File.last_modified.desc())
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def get_files_by_source_paginated(self, source_id: int, skip: int = 0, limit: int = 100) -> List[File]:
        stmt = select(File).where(File.source_id == source_id).order_by(File.last_modified.desc()).offset(skip).limit(
            limit)
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def full_duplicate_files(self, file_hash: str) -> List[File]:
        stmt = select(File).where(File.file_hash == file_hash).order_by(File.last_modified.desc())
        res = self.__session.execute(stmt)
        return res.scalars().all()

    def delete_file(self, file_id: int) -> bool:
        file = self.get_file_by_id(file_id)
        if not file:
            return False

        self.__session.delete(file)
        self.__session.commit()
        return True

    def create_tag(self,
                   tag_name: str,
                   tag_type: str = 'manual',
                   description: Optional[str] = None
                   ) -> Tag:
        db_tag = Tag(
            tag_name=tag_name,
            tag_type=tag_type,
            description=description
        )

        self.__session.add(db_tag)
        self.__session.commit()
        self.__session.refresh(db_tag)

        return db_tag

    def add_tag_to_file(self, file_id: int, tag_id: int, assigned_by: Optional[int] = None) -> FileTag:
        file_tag = FileTag(
            file_id=file_id,
            tag_id=tag_id,
            assigned_by=assigned_by
        )
        self.__session.add(file_tag)
        self.__session.commit()
        self.__session.refresh(file_tag)
        return file_tag

    def remove_tag_from_file(self, file_id: int, tag_id: int) -> bool:
        stmt = select(FileTag).where(FileTag.file_id == file_id, FileTag.tag_id == tag_id)
        result = self.__session.execute(stmt)
        file_tag = result.scalar_one_or_none()

        if not file_tag:
            return False

        self.__session.delete(file_tag)
        self.__session.commit()
        return True

    def get_file_tags(self, file_id: int) -> List[Tag]:
        stmt = select(Tag).join(FileTag, Tag.id == FileTag.tag_id).where(FileTag.file_id == file_id).order_by(Tag.id)
        result = self.__session.execute(stmt)
        return result.scalars().all()

    def get_files_count_by_user(self, user_id: int) -> int:
        stmt = select(func.count(File.id)).where(File.user_id == user_id)
        res = self.__session.execute(stmt)
        return res.scalar()

    def get_files_by_filters(
            self,
            user_id: Optional[int] = None,
            file_type: Optional[str] = None,
            tags: Optional[List[str]] = None,
            counterparty: Optional[str] = None
    ) -> List[File]:

        query = self.__session.query(File)
        print(query)
        if user_id:
            query = query.filter(File.user_id == user_id)
        if file_type:
            query = query.filter(File.file_type == file_type)
        all_tags = []
        if tags:
            all_tags.extend(tags)
        if counterparty:
            all_tags.append(counterparty)
        if all_tags:
            for tag_name in all_tags:
                query = query.filter(File.tags.any(tag_name=tag_name))
        return query.all()
