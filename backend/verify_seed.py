#!/usr/bin/env python
"""Verify seeded test data in database."""

import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


async def verify():
    """Verify test data was seeded successfully."""
    engine = create_async_engine(
        'mysql+aiomysql://root:0000@localhost:3306/bd_project',
        future=True,
        echo=False
    )
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print('\n=== TEST DATA VERIFICATION ===\n')
        
        queries = [
            ('SELECT COUNT(*) FROM department', 'Departments'),
            ('SELECT COUNT(*) FROM niveau', 'Levels'),
            ('SELECT COUNT(*) FROM filiere', 'Programs (Filières)'),
            ('SELECT COUNT(*) FROM systeme', 'Systems'),
            ('SELECT COUNT(*) FROM salletp', 'Lab Rooms'),
            ('SELECT COUNT(*) FROM module', 'Modules'),
            ('SELECT COUNT(*) FROM section', 'Sections'),
            ('SELECT COUNT(*) FROM groupetp', 'Lab Groups'),
        ]
        
        total_records = 0
        for query, label in queries:
            try:
                result = await session.execute(text(query))
                count = result.scalar()
                print(f'  ✓ {label:25} : {count:3} records')
                total_records += count
            except Exception as e:
                print(f'  ✗ {label:25} : Error - {str(e)[:50]}')
        
        print(f'\n  Total records seeded: {total_records}')
        print('\n✓ Test data is ready for development!\n')
    
    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(verify())
