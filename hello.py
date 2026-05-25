# A dictionary — labelled drawers instead of numbered positions
customers = [ 
    {"name": "Oladeji", "income": 80000, "loan": 200000, "account": "Premium", "city": "Ontario"},
    {"name": "Tunde",   "income": 30000, "loan": 100000, "account": "Basic", "city": "Texas"},
    {"name": "Amaka",   "income": 100000, "loan": 250000, "account": "Premium", "city": "Chicago"},
    {"name": "Chidi",   "income": 60000, "loan": 150000, "account": "Basic", "city": "Lagos"},
    {"name": "Ngozi",   "income": 45000, "loan": 90000,  "account": "Basic", "city": "Lome"},
]


def process_customer(c):
    max_loan = c["income"] * 3
    approved = c["income"] >= 50000 and c["loan"] <= max_loan

    status = "APPROVED ✓" if approved else "REJECTED ✗"
    
    print("Name: "    + c["name"])
    print("Account: " + c["account"])
    print("Status: "  + status)
    print("city:" + c["city"])
    print("---")

# Loop through the entire database
for customer in customers:
    process_customer(customer)