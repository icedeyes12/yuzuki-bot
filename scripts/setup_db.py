#!/usr/bin/env python3
"""Setup PostgreSQL database for Yuzuki."""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "yuzuki")
DB_USER = os.getenv("DB_USER", "yuzuki")
DB_PASS = os.getenv("DB_PASS")

async def _create_tables():
    from shared.database import db
    await db.connect()
    await db.create_tables()
    print("✅ Database tables created!")
    print("\nTables:")
    print("  - users: User profiles and facts")
    print("  - blocked_users: Blocked user log")
    print("  - messages: All message history")
    print("  - memories: Extracted facts about users")
    print("  - conversations: Thread contexts")
    await db.close()

async def setup():
    import asyncpg

    print("🗄️  Setting up Yuzuki database...")

    if not DB_PASS:
        print("❌ DB_PASS not set. Copy .env.example to .env and fill in values.")
        sys.exit(1)

    # Connect to default 'postgres' DB to create yuzuki DB and user
    sys.stdout.write("Creating database and user... ")
    sys.stdout.flush()
    try:
        default_conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            database="postgres",
            user=DB_USER,
            password=DB_PASS,
        )
        try:
            # Create user (ignore error if exists)
            await default_conn.execute(
                f'CREATE USER {DB_USER} WITH PASSWORD $1',
                DB_PASS,
            )
        except asyncpg.DuplicateObjectError:
            pass

        # Create database (ignore error if exists)
        try:
            await default_conn.execute(f'CREATE DATABASE {DB_NAME} OWNER {DB_USER}')
        except asyncpg.DuplicateDatabaseError:
            pass

        await default_conn.close()
        print("done!")
    except Exception as e:
        print(f"warning: could not create DB/user (may already exist): {e}")

    # Now create tables in the yuzuki DB
    print("Creating tables... ")
    await _create_tables()

    print("\n🎉 Setup complete!")
    print(f"   Database: {DB_NAME}")
    print(f"   User: {DB_USER}")
    print(f"   Host: {DB_HOST}:{DB_PORT}")

if __name__ == "__main__":
    asyncio.run(setup())