import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import random
from datetime import datetime, timedelta
load_dotenv()

class DisasterManagementDB:
    def __init__(self):
        self.connection = None
        self.connect_db()
        self.seed_data()

    def connect_db(self):
        try:
            self.connection = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)
            print("✅ Connected to Neon PostgreSQL successfully.")
        except Exception as e:
            print(f"❌ Error connecting to the database: {e}")

    def create_tables(self):
        try:
            with self.connection.cursor() as cursor:
                with open("tables.sql", "r") as file:
                    commands = file.read().split(";")
                    for command in commands:
                        cmd = command.strip()
                        if cmd:
                            cursor.execute(cmd)
                            print(f"Executed SQL command: \n{cmd}")
                self.connection.commit()
                print("✅ Tables created successfully.")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")

    def seed_data(self):
        def random_date(days_ago):
            return datetime.now() - timedelta(days=random.randint(1, days_ago))

        def random_severity():
            return random.randint(1, 5)

        def random_disaster_type():
            return random.choice(['Flood', 'Cyclone', 'Earthquake', 'Heatwave', 'Landslide'])

        def random_location():
            return random.choice([
                'Mumbai, India', 'Chennai, India', 'Delhi, India',
                'Kolkata, India', 'Bangalore, India', 'Hyderabad, India'
            ])

        try:
            with self.connection.cursor() as cur:
                # Clear old data for clean reseeding (optional)
                cur.execute("DELETE FROM disaster_reports")
                cur.execute("DELETE FROM disaster_news")
                cur.execute("DELETE FROM relief_resources")
                cur.execute("DELETE FROM resource_allocation")
                cur.execute("DELETE FROM donations")
                cur.execute("DELETE FROM safety_policies")

                # Seed disaster reports
                for _ in range(10):
                    cur.execute("""
                        INSERT INTO disaster_reports (location, disaster_type, report_date, severity)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        random_location(),
                        random_disaster_type(),
                        random_date(30),
                        random_severity()
                    ))

                # Seed disaster news
                for _ in range(5):
                    title = f"{random_disaster_type()} Alert in {random_location()}"
                    summary = "Automatically generated alert for testing dashboard visuals."
                    content = f"This is the full content for: {title}. Stay alert and follow instructions from local authorities."

                    cur.execute("""
                                INSERT INTO disaster_news (title, news_type, publish_date, location, severity, content, summary)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """, (
                                    title,
                                    random.choice(['warning', 'update', 'prediction']),
                                    random_date(20),
                                    random_location(),
                                    random_severity(),
                                    content,
                                    summary
                                ))

                relief_resources = [
                    ('Food Packets', 1500),
                    ('Water Bottles', 2500),
                    ('Medical Kits', 500)
                ]
                resource_ids = []
                for name, qty in relief_resources:
                    cur.execute("""
                                INSERT INTO relief_resources (resource_name, quantity_available, last_updated)
                                VALUES (%s, %s, CURRENT_DATE) RETURNING resource_id
                                """, (name, qty))
                    resource_ids.append(cur.fetchone()["resource_id"])

                # Insert resource allocations using fetched resource_ids
                cur.execute("""
                                INSERT INTO relief_resources (resource_name, quantity, unit, cost_per_unit, last_updated)
VALUES 
    ('Blankets', 800, 'pieces', 120.00, CURRENT_DATE),
    ('Tents', 150, 'units', 2500.00, CURRENT_DATE),
    ('Sanitary Napkins', 3000, 'packs', 20.00, CURRENT_DATE),
    ('Mosquito Nets', 1000, 'units', 150.00, CURRENT_DATE),
    ('Flashlights', 500, 'pieces', 75.00, CURRENT_DATE),
    ('Battery Packs', 300, 'units', 500.00, CURRENT_DATE),
    ('Infant Formula', 400, 'cans', 250.00, CURRENT_DATE),
    ('Drinking Water Tanks', 20, 'tanks', 10000.00, CURRENT_DATE),
    ('Emergency Rations', 2000, 'packs', 40.00, CURRENT_DATE),
    ('First Aid Kits', 350, 'kits', 300.00, CURRENT_DATE);

                                """)

                # Donations
                cur.execute("""
                    INSERT INTO donations (donor_name, donor_email, amount, donation_date, disaster_id)
                    VALUES ('Aamir Khan', 'aamir@example.com', 10000, CURRENT_DATE - INTERVAL '5 days', 1),
                           ('Rita Patel', 'rita@example.com', 5000, CURRENT_DATE - INTERVAL '3 days', 2),
                           ('Global Relief Org', 'relief@ngo.org', 25000, CURRENT_DATE - INTERVAL '1 day', 3);
                """)

                # Safety Policies
                cur.execute("""
                            INSERT INTO safety_policies (title, disaster_type, content, priority)
                            VALUES ('Evacuation Plan for Coastal Areas', 'Cyclone',
                                    'Detailed evacuation routes and shelters', 'High'),
                                   ('Water Purification Guidelines', 'Flood',
                                    'Steps to ensure clean drinking water after floods', 'Medium'),
                                   ('Heatwave Safety Tips', 'Heatwave', 'Instructions to prevent heat strokes', 'Low');
                            """)

                self.connection.commit()
                print("✅ Database seeded with sample data.")
        except Exception as e:
            print("❌ Failed to seed data:", e)

    def get_dashboard_stats(self):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Total number of disasters
                cursor.execute("SELECT COUNT(*) AS total_disasters FROM disaster_reports")
                disasters = cursor.fetchone()["total_disasters"]

                # Total donations
                cursor.execute("SELECT COUNT(*) AS total_donations FROM donations")
                donations = cursor.fetchone()["total_donations"]

                # Total policies
                cursor.execute("SELECT COUNT(*) AS total_policies FROM safety_policies")
                policies = cursor.fetchone()["total_policies"]

                # Severity distribution
                cursor.execute("SELECT severity, COUNT(*) FROM disaster_reports GROUP BY severity")
                severity_data = cursor.fetchall()

                # ✅ Total resource types
                cursor.execute("SELECT COUNT(*) AS total_resource_types FROM relief_resources")
                resource_types = cursor.fetchone()["total_resource_types"]

                # ✅ Total quantity available across all resources
                cursor.execute("SELECT SUM(quantity) AS total_resource_quantity FROM relief_resources")
                total_quantity = cursor.fetchone()["total_resource_quantity"] or 0

                return {
                    "total_disasters": disasters,
                    "total_donations": donations,
                    "total_policies": policies,
                    "severity_distribution": severity_data,
                    "total_resource_types": resource_types,
                    "total_resource_quantity": total_quantity
                }

        except Exception as e:
            print(f"❌ Error fetching dashboard stats: {e}")
            return {}

    def add_donation(self, donation):
        try:
            with self.connection.cursor() as cur:
                cur.execute("""
                            INSERT INTO donations (donor_name, donor_email, amount, donation_date, disaster_id, message)
                            VALUES (%s, %s, %s, CURRENT_DATE, %s, %s)
                            """, (
                                donation.donor_name,
                                donation.donor_email,
                                donation.amount,
                                donation.disaster_id,
                                donation.message
                            ))
                self.connection.commit()
                return True
        except Exception as e:
            print(f"❌ Error inserting donation: {e}")
            return False

    def get_disaster_reports(self, timeframe="monthly"):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                        SELECT *, severity::int \
                        FROM disaster_reports \
                        """
                if timeframe == "monthly":
                    query += " WHERE report_date >= NOW() - INTERVAL '1 month'"
                elif timeframe == "weekly":
                    query += " WHERE report_date >= NOW() - INTERVAL '7 days'"
                elif timeframe == "yearly":
                    query += " WHERE report_date >= NOW() - INTERVAL '1 year'"

                query += " ORDER BY report_date DESC"
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching disaster reports: {e}")
            return []

    def get_disaster_news(self, news_type=None):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM disaster_news"
                if news_type:
                    query += " WHERE news_type = %s"
                    cursor.execute(query, (news_type,))
                else:
                    cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print("Error loading disaster news:", e)
            return []

    def get_donations(self, limit=10):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM donations
                    ORDER BY donation_date DESC
                    LIMIT %s
                """, (limit,))
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching donations: {e}")
            return []

    def get_safety_policies(self, disaster_type=None):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM safety_policies"
                if disaster_type:
                    query += " WHERE disaster_type = %s"
                    cursor.execute(query, (disaster_type,))
                else:
                    cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print("Error loading safety policies:", e)
            return []

    def get_relief_resources(self):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM relief_resources")
                return cursor.fetchall()
        except Exception as e:
            print("Error loading relief resources:", e)
            return []

    def get_total_donations(self):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT SUM(amount) FROM donations")
                result = cursor.fetchone()
                return result["sum"] if result["sum"] is not None else 0
        except Exception as e:
            print("Error loading donation total:", e)
            return 0

    def get_resource_allocations(self):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                               SELECT ra.allocation_id,
                                      dr.location,
                                      rr.resource_name,
                                      ra.allocated_quantity,
                                      ra.allocation_date
                               FROM resource_allocation ra
                                        JOIN disaster_reports dr ON ra.report_id = dr.report_id
                                        JOIN relief_resources rr ON ra.resource_id = rr.resource_id
                               ORDER BY ra.allocation_date DESC
                               """)
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error loading resource allocations: {e}")
            return []


db = DisasterManagementDB()
