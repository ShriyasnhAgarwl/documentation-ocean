import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import sys
import os

# Adjust path to import settings if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.config import get_settings

async def migrate_telegram_to_sites():
    print("Starting Telegram configuration migration...")
    settings = get_settings()
    
    print(f"Connecting to MongoDB at {settings.MONGO_URL.split('@')[-1] if '@' in settings.MONGO_URL else 'localhost'}...")
    client = AsyncIOMotorClient(settings.MONGO_URL)
    db = client[settings.mongo_db]
    
    companies_collection = db["companies"]
    sites_collection = db["sites"]

    # Find companies that have a telegram configuration configured
    companies_with_telegram = companies_collection.find({
        "telegram.telegram_bot_token": {"$exists": True, "$ne": ""},
        "telegram.telegram_chat_id": {"$exists": True, "$ne": ""}
    })
    
    companies_count = await companies_collection.count_documents({
        "telegram.telegram_bot_token": {"$exists": True, "$ne": ""},
        "telegram.telegram_chat_id": {"$exists": True, "$ne": ""}
    })
    
    print(f"Found {companies_count} companies with a Telegram configuration.")

    migrated_sites_total = 0
    
    async for company in companies_with_telegram:
        company_id = company["_id"]
        telegram_config = company.get("telegram")
        
        print(f"Migrating for company ID: {company_id}...")
        
        # Update all sites belonging to this company that don't already have a telegram configuration
        result = await sites_collection.update_many(
            {
                "company_id": company_id,
                "telegram": {"$exists": False} # Only add if not already set manually on the site
            },
            {
                "$set": {
                    "telegram": {
                        "telegram_bot_token": telegram_config.get("telegram_bot_token"),
                        "telegram_chat_id": telegram_config.get("telegram_chat_id")
                    }
                }
            }
        )
        
        print(f"  - Updated {result.modified_count} site(s) for company {company_id}.")
        migrated_sites_total += result.modified_count
        
        # Optionally, clean up the company collection by unsetting the old telegram field.
        # Uncomment the lines below if you want to perform cleanup after successful migration.
        """
        cleanup_result = await companies_collection.update_one(
            {"_id": company_id},
            {"$unset": {"telegram": 1}}
        )
        print(f"  - Removed old telegram config from company {company_id}.")
        """

    print(f"\nMigration completed successfully!")
    print(f"Total sites updated with Telegram configuration: {migrated_sites_total}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(migrate_telegram_to_sites())
