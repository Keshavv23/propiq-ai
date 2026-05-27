import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.orm import Agency, Listing
import random

Base.metadata.create_all(bind=engine)

AGENCIES = [
    {"name": "Sharma Properties", "email": "sharma@properties.com", "phone": "9876543210", "city": "Indore"},
    {"name": "Mumbai Realty Group", "email": "info@mumbairealty.com", "phone": "9821234567", "city": "Mumbai"},
    {"name": "Pune Homes", "email": "contact@punehomes.com", "phone": "9765432109", "city": "Pune"},
    {"name": "Bangalore Spaces", "email": "hello@bangalorespaces.com", "phone": "9900112233", "city": "Bangalore"},
    {"name": "Indore Estates", "email": "admin@indoreestates.com", "phone": "9111222333", "city": "Indore"},
]

LISTINGS = [
    # Indore
    {"title": "2 BHK Flat in Vijay Nagar", "city": "Indore", "locality": "Vijay Nagar", "price": 4500000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 950, "property_type": "flat", "description": "Well maintained 2 BHK flat in the heart of Vijay Nagar. Close to D-Mart and schools. Society with 24/7 security and parking."},
    {"title": "3 BHK Flat in Scheme 54", "city": "Indore", "locality": "Scheme 54", "price": 7200000, "bedrooms": 3, "bathrooms": 2, "area_sqft": 1350, "property_type": "flat", "description": "Spacious 3 BHK in premium Scheme 54 locality. Modular kitchen, marble flooring, covered parking. Walking distance to Treasure Island Mall."},
    {"title": "1 BHK Flat in Palasia", "city": "Indore", "locality": "Palasia", "price": 2800000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 550, "property_type": "flat", "description": "Compact 1 BHK ideal for working professionals. Prime Palasia location, all amenities nearby."},
    {"title": "4 BHK Villa in Nipania", "city": "Indore", "locality": "Nipania", "price": 18000000, "bedrooms": 4, "bathrooms": 3, "area_sqft": 2800, "property_type": "villa", "description": "Luxurious independent villa in Nipania. Private garden, 2 car parking, servant quarters. Gated community with club house."},
    {"title": "2 BHK Flat in MR-10", "city": "Indore", "locality": "MR-10", "price": 5100000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 1050, "property_type": "flat", "description": "Modern 2 BHK on MR-10 road. Vastu compliant, east facing, lift and power backup available."},
    {"title": "Plot in Rau", "city": "Indore", "locality": "Rau", "price": 3200000, "bedrooms": 0, "bathrooms": 0, "area_sqft": 1200, "property_type": "plot", "description": "Residential plot in fast developing Rau area. NA approved, near highway, clear title."},
    {"title": "3 BHK Flat in Sudama Nagar", "city": "Indore", "locality": "Sudama Nagar", "price": 6500000, "bedrooms": 3, "bathrooms": 2, "area_sqft": 1250, "property_type": "flat", "description": "Corner flat with 3 BHK in Sudama Nagar. Two balconies, great ventilation, society amenities."},
    {"title": "Commercial Shop in Rajwada", "city": "Indore", "locality": "Rajwada", "price": 9500000, "bedrooms": 0, "bathrooms": 1, "area_sqft": 400, "property_type": "commercial", "description": "Prime commercial shop near Rajwada. High footfall area, ground floor, ideal for retail or office."},
    {"title": "2 BHK in Bhawarkuan", "city": "Indore", "locality": "Bhawarkuan", "price": 4200000, "bedrooms": 2, "bathrooms": 1, "area_sqft": 880, "property_type": "flat", "description": "Ready to move 2 BHK near Bhawarkuan Square. Good connectivity to airport and railway station."},
    {"title": "3 BHK Villa in Super Corridor", "city": "Indore", "locality": "Super Corridor", "price": 12500000, "bedrooms": 3, "bathrooms": 3, "area_sqft": 2200, "property_type": "villa", "description": "Modern villa on Super Corridor. Near IIM Indore and IT parks. Perfect for professionals."},

    # Mumbai
    {"title": "1 BHK Flat in Andheri West", "city": "Mumbai", "locality": "Andheri West", "price": 9500000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 450, "property_type": "flat", "description": "Compact 1 BHK in Andheri West. Close to metro station and Link Road. Ideal for working professionals."},
    {"title": "2 BHK Flat in Powai", "city": "Mumbai", "locality": "Powai", "price": 16500000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 850, "property_type": "flat", "description": "Premium 2 BHK in Powai with lake view. Gated complex with gym, pool and 24/7 security."},
    {"title": "3 BHK in Borivali East", "city": "Mumbai", "locality": "Borivali East", "price": 18000000, "bedrooms": 3, "bathrooms": 2, "area_sqft": 1100, "property_type": "flat", "description": "Spacious 3 BHK near Borivali station. National Park views, excellent connectivity."},
    {"title": "1 BHK in Thane West", "city": "Mumbai", "locality": "Thane West", "price": 7200000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 520, "property_type": "flat", "description": "Affordable 1 BHK in Thane West. New building, amenities like gym and play area included."},
    {"title": "2 BHK in Kandivali East", "city": "Mumbai", "locality": "Kandivali East", "price": 11500000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 750, "property_type": "flat", "description": "Well located 2 BHK in Kandivali East. Metro connectivity, near schools and hospitals."},
    {"title": "Studio in Lower Parel", "city": "Mumbai", "locality": "Lower Parel", "price": 8500000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 380, "property_type": "flat", "description": "Modern studio apartment in Lower Parel. Walking distance to office hubs and restaurants."},
    {"title": "3 BHK in Mulund West", "city": "Mumbai", "locality": "Mulund West", "price": 19500000, "bedrooms": 3, "bathrooms": 3, "area_sqft": 1250, "property_type": "flat", "description": "Luxury 3 BHK in Mulund West with mountain views. Premium fittings, covered parking."},
    {"title": "Commercial Office in BKC", "city": "Mumbai", "locality": "Bandra Kurla Complex", "price": 45000000, "bedrooms": 0, "bathrooms": 2, "area_sqft": 1200, "property_type": "commercial", "description": "Grade A office space in BKC. Ready to use, fully furnished, metro access."},
    {"title": "2 BHK in Malad West", "city": "Mumbai", "locality": "Malad West", "price": 12000000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 780, "property_type": "flat", "description": "Ready possession 2 BHK in Malad West. Society with clubhouse and kids play area."},
    {"title": "4 BHK in Juhu", "city": "Mumbai", "locality": "Juhu", "price": 65000000, "bedrooms": 4, "bathrooms": 4, "area_sqft": 2400, "property_type": "flat", "description": "Ultra luxury 4 BHK near Juhu beach. Private terrace, home theatre, sea facing rooms."},

    # Pune
    {"title": "2 BHK in Baner", "city": "Pune", "locality": "Baner", "price": 8500000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 950, "property_type": "flat", "description": "Modern 2 BHK in Baner IT corridor. Close to Balewadi and Hinjewadi. Great investment."},
    {"title": "3 BHK in Kothrud", "city": "Pune", "locality": "Kothrud", "price": 12000000, "bedrooms": 3, "bathrooms": 2, "area_sqft": 1350, "property_type": "flat", "description": "Premium 3 BHK in sought-after Kothrud. Near law college road, excellent neighbourhood."},
    {"title": "1 BHK in Wakad", "city": "Pune", "locality": "Wakad", "price": 4800000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 580, "property_type": "flat", "description": "Affordable 1 BHK in Wakad near Hinjewadi IT park. Perfect for IT professionals."},
    {"title": "Villa in Koregaon Park", "city": "Pune", "locality": "Koregaon Park", "price": 35000000, "bedrooms": 4, "bathrooms": 4, "area_sqft": 3200, "property_type": "villa", "description": "Prestigious villa in Koregaon Park. Tree lined street, private pool, premium finishes."},
    {"title": "2 BHK in Hadapsar", "city": "Pune", "locality": "Hadapsar", "price": 6200000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 890, "property_type": "flat", "description": "Affordable 2 BHK near Magarpatta City. Good rental income potential, near IT parks."},
    {"title": "Plot in Wagholi", "city": "Pune", "locality": "Wagholi", "price": 4500000, "bedrooms": 0, "bathrooms": 0, "area_sqft": 1500, "property_type": "plot", "description": "NA approved residential plot in Wagholi. Fast developing area, near Kharadi IT hub."},
    {"title": "3 BHK in Aundh", "city": "Pune", "locality": "Aundh", "price": 14500000, "bedrooms": 3, "bathrooms": 3, "area_sqft": 1480, "property_type": "flat", "description": "Luxury 3 BHK in prime Aundh location. Rooftop amenities, gym, concierge service."},
    {"title": "2 BHK in Viman Nagar", "city": "Pune", "locality": "Viman Nagar", "price": 9800000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 1020, "property_type": "flat", "description": "Well maintained 2 BHK in Viman Nagar. Close to airport, malls and restaurants."},
    {"title": "Commercial in FC Road", "city": "Pune", "locality": "FC Road", "price": 22000000, "bedrooms": 0, "bathrooms": 1, "area_sqft": 800, "property_type": "commercial", "description": "High street commercial space on FC Road. Excellent footfall, suitable for cafe or retail."},
    {"title": "1 BHK in Pimple Saudagar", "city": "Pune", "locality": "Pimple Saudagar", "price": 5500000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 620, "property_type": "flat", "description": "Compact 1 BHK in Pimple Saudagar. Near Pune University and IT companies."},

    # Bangalore
    {"title": "2 BHK in Whitefield", "city": "Bangalore", "locality": "Whitefield", "price": 9200000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 1050, "property_type": "flat", "description": "Modern 2 BHK in Whitefield IT hub. Gated community with pool and gym. Metro coming soon."},
    {"title": "3 BHK in Koramangala", "city": "Bangalore", "locality": "Koramangala", "price": 18500000, "bedrooms": 3, "bathrooms": 3, "area_sqft": 1600, "property_type": "flat", "description": "Premium 3 BHK in vibrant Koramangala. Walking to restaurants, startups, metro station."},
    {"title": "1 BHK in Electronic City", "city": "Bangalore", "locality": "Electronic City", "price": 4200000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 580, "property_type": "flat", "description": "Budget 1 BHK near Electronic City Phase 1. Ideal for Infosys and Wipro employees."},
    {"title": "Villa in Sarjapur Road", "city": "Bangalore", "locality": "Sarjapur Road", "price": 28000000, "bedrooms": 4, "bathrooms": 4, "area_sqft": 3000, "property_type": "villa", "description": "Gated villa community on Sarjapur Road. Clubhouse, tennis court, 24/7 security."},
    {"title": "2 BHK in HSR Layout", "city": "Bangalore", "locality": "HSR Layout", "price": 11500000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 1100, "property_type": "flat", "description": "Spacious 2 BHK in HSR Layout. Close to tech parks and startup ecosystem."},
    {"title": "3 BHK in Indiranagar", "city": "Bangalore", "locality": "Indiranagar", "price": 22000000, "bedrooms": 3, "bathrooms": 3, "area_sqft": 1750, "property_type": "flat", "description": "Luxury 3 BHK in premium Indiranagar. Walking distance to 100 Feet Road and metro."},
    {"title": "Plot in Devanahalli", "city": "Bangalore", "locality": "Devanahalli", "price": 6800000, "bedrooms": 0, "bathrooms": 0, "area_sqft": 2400, "property_type": "plot", "description": "Residential plot near Bangalore airport. BMRDA approved, fast appreciating area."},
    {"title": "2 BHK in Marathahalli", "city": "Bangalore", "locality": "Marathahalli", "price": 7800000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 980, "property_type": "flat", "description": "Ready to move 2 BHK in Marathahalli. Near Outer Ring Road IT corridor."},
    {"title": "Commercial in MG Road", "city": "Bangalore", "locality": "MG Road", "price": 38000000, "bedrooms": 0, "bathrooms": 2, "area_sqft": 1100, "property_type": "commercial", "description": "Prime commercial space on MG Road. Metro adjacent, high visibility location."},
    {"title": "1 BHK in Hebbal", "city": "Bangalore", "locality": "Hebbal", "price": 5200000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 620, "property_type": "flat", "description": "Affordable 1 BHK in Hebbal near flyover. Quick access to airport and city centre."},
    {"title": "4 BHK in JP Nagar", "city": "Bangalore", "locality": "JP Nagar", "price": 24000000, "bedrooms": 4, "bathrooms": 3, "area_sqft": 2200, "property_type": "flat", "description": "Spacious 4 BHK in JP Nagar Phase 1. Quiet locality, good schools nearby, vastu compliant."},

    # Mixed extra listings
    {"title": "2 BHK in Navi Mumbai", "city": "Mumbai", "locality": "Navi Mumbai", "price": 8200000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 920, "property_type": "flat", "description": "Affordable 2 BHK in Navi Mumbai. Near Vashi station, wide roads, planned township."},
    {"title": "3 BHK in Hinjewadi", "city": "Pune", "locality": "Hinjewadi", "price": 11000000, "bedrooms": 3, "bathrooms": 2, "area_sqft": 1380, "property_type": "flat", "description": "IT hub 3 BHK in Hinjewadi Phase 2. Ideal for professionals working in Infosys, TCS, Wipro."},
    {"title": "2 BHK in Begur Road", "city": "Bangalore", "locality": "Begur Road", "price": 6500000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 1020, "property_type": "flat", "description": "Value for money 2 BHK on Begur Road. New project, OC received, immediate possession."},
    {"title": "Plot in Depalpur", "city": "Indore", "locality": "Depalpur", "price": 1800000, "bedrooms": 0, "bathrooms": 0, "area_sqft": 2000, "property_type": "plot", "description": "Agricultural to residential converted plot in Depalpur. Good for long term investment."},
    {"title": "3 BHK in Chembur", "city": "Mumbai", "locality": "Chembur", "price": 21000000, "bedrooms": 3, "bathrooms": 2, "area_sqft": 1150, "property_type": "flat", "description": "Premium 3 BHK in Chembur. Monorail and metro connectivity, upcoming infrastructure boost."},
    {"title": "2 BHK in Bavdhan", "city": "Pune", "locality": "Bavdhan", "price": 7800000, "bedrooms": 2, "bathrooms": 2, "area_sqft": 990, "property_type": "flat", "description": "Peaceful 2 BHK in Bavdhan hills area. Green surroundings, near Kothrud and Chandni Chowk."},
    {"title": "Villa in Yelahanka", "city": "Bangalore", "locality": "Yelahanka", "price": 22000000, "bedrooms": 3, "bathrooms": 3, "area_sqft": 2600, "property_type": "villa", "description": "Independent villa in Yelahanka. Near new town, airport road, CBSE schools."},
    {"title": "1 BHK in Indore Bypass", "city": "Indore", "locality": "Bypass Road", "price": 3200000, "bedrooms": 1, "bathrooms": 1, "area_sqft": 620, "property_type": "flat", "description": "Budget 1 BHK on AB Bypass Road. New construction, ready possession, near Ring Road."},
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(Agency).count()
        if existing > 0:
            print(f"Database already has {existing} agencies. Skipping seed.")
            print("To reseed, delete all rows from agencies and listings tables first.")
            return

        print("Seeding agencies...")
        agency_objects = []
        for a in AGENCIES:
            agency = Agency(**a)
            db.add(agency)
            agency_objects.append(agency)
        db.flush()

        print("Seeding listings...")
        for i, l in enumerate(LISTINGS):
            agency = agency_objects[i % len(agency_objects)]
            listing = Listing(**l, agency_id=agency.id)
            db.add(listing)

        db.commit()
        print(f"Done! Inserted {len(AGENCIES)} agencies and {len(LISTINGS)} listings.")
        print("Open your Supabase Table Editor to see the data.")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()