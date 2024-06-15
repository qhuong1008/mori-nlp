import random
from datetime import datetime, timedelta
import json

book_ids = [
    "653cbbf4f64340dfdb355c0e",  # 0
    "653cbbf4f64340dfdb355c0f",  # 1
    "653cbbf4f64340dfdb355c10",  # 2
    "653cbbf4f64340dfdb355c12",  # 3
    "653cbbf4f64340dfdb355c13",  # 4
    "653cbbf4f64340dfdb355c14",  # 5
    "653cbbf4f64340dfdb355c16",  # 6
    "653cbbf4f64340dfdb355c17",  # 7
    "653cbbf4f64340dfdb355c18",  # 8
    "653cbbf4f64340dfdb355c19",  # 9
    "653cbbf4f64340dfdb355c1a",  # 10
    "653cbbf4f64340dfdb355c1b",  # 11
    "653cbbf4f64340dfdb355c1c",  # 12
    "6562165148002057d2ce8be1",  # 13
    "656b7445cdff5da854543c1c",  # 14
    "656eef18a09708917971ab2b",  # 15
    "656f520122a703c9be4ebcb0",  # 16
    "656f5e1422a703c9be4ebd01",  # 17
    "6570bfb8080acd8b8e1c2fd7",  # 18
    "65757e0bc477d623c57ace43",  # 19
    "65757f84c477d623c57ace5c",  # 20
    "65807a589eac8d942b0d7647",  # 21
    "658080009eac8d942b0d7655",  # 22
    "65931ea4b5ef833d7a86240e",  # 23
    "6593247bb86e7e4835e66a82",  # 24
    "65932d1dff7f147158b2028a",  # 25
    "65932f00ff7f147158b20292",  # 26
    "65933086ff7f147158b20363",  # 27
    "659330e9ff7f147158b2036c",  # 28
    "6593316cff7f147158b20375",  # 29
    "659331e4ff7f147158b2037e",  # 30
    "65933245ff7f147158b20383",  # 31
    "6593328fff7f147158b20388",  # 32
    "659332e8ff7f147158b20391",  # 33
    "65933324ff7f147158b20396",  # 34
    "6593336fff7f147158b2039b",  # 35
    "65933418ff7f147158b203a0",  # 36
    "6593350dff7f147158b20491",  # 37
    "65933557ff7f147158b20496",  # 38
    "659335e2ff7f147158b20500",  # 39
    "65933699ff7f147158b2050b",  # 40
    "659338c6ff7f147158b20599",  # 41
    "664c4e12badfedddea88a939",  # 42
    "664c5a7f38670415ba0a2560",  # 43
    "664c86ca38670415ba0a2587",  # 44
    "664c89478de582782e625255",  # 45
    "664c8bbf63d703a7512b8d57",  # 46
    "664c8ccacebac1bdbb822e39",  # 47
    "664c8dc5ceefe1cc786fa90e",  # 48
    "664c8fc504a463570189a36b",  # 49
    "664c92709348b02c284ab16a",  # 50
    "664c95c134e9d01f77e6f1b6",  # 51
    "664c9a2990e39828b3b4593c",  # 52
    "664c9cedc38403ed782f44a5",  # 53
    "664ca0ec8179762b1337d32e",  # 54
    "664ca3038a68628a5a1b2e90",  # 55
    "664ca889daddbd8c3afbfc42",  # 56
    "664cb0df8d3b900945e1dce5",  # 57
    "664cb2929c4e525f8eeb419d",  # 58
]

interest_groups = {
    "self_help": [0, 1, 7, 8, 10, 13, 14, 15, 16, 18, 44, 48],
    "philosophy_spirituality": [4, 5, 11, 12, 19, 17, 35],
    "health_psychology": [2, 24, 32, 28, 34, 21, 56],
    "relationships_love": [3, 27, 29, 30, 33, 50, 57],
    "business_sales": [20, 53, 55],
    "literature_fiction": [
        9, 23, 36, 37, 38, 39, 40, 41, 25, 42, 43, 49, 51, 52, 58,
    ],
    "exploration_unique": [22, 45, 46, 47, 6, 31, 54],
}

# Sinh dữ liệu giả cho tài khoản
def generate_fake_accounts(num_accounts):
    accounts = []
    for i in range(num_accounts):
        accounts.append({
            "_id": f"account{i+1}",
            "username": f"user{i+1}",
            "password": "hashed_password",
            "email": f"user{i+1}@example.com",
            "displayName": f"User {i+1}",
            "phoneNumber": f"01234567{89-i}",
            "avatar": "avt.jpg",
            "role": 0,
            "is_member": random.choice([True, False]),
            "is_blocked": False,
            "is_active": True,
            "is_verify_email": random.choice([True, False]),
            "passwordResetToken": None,
            "passwordResetExpires": None,
            "recommendations": []
        })
    return accounts

# Sinh dữ liệu giả cho đánh giá dựa trên sở thích
def generate_fake_reviews(num_reviews, num_accounts, interest_groups):
    reviews = []
    for i in range(num_reviews):
        user_id = f"account{random.randint(1, num_accounts)}"
        interest_group = random.choice(list(interest_groups.keys()))
        book_id = random.choice(interest_groups[interest_group])
        rating = random.randint(4, 5) if random.random() < 0.7 else random.randint(1, 3)
        content = "Rất hay!" if rating >= 4 else "Bình thường." if rating == 3 else "Không hay."
        posted_date = datetime.now() - timedelta(days=random.randint(0, 365))
        reviews.append({
            "user": user_id,
            "book_id": book_ids[book_id],
            "rating": rating,
            "content": content,
            "postedDate": posted_date.isoformat() + "Z",
            "liked": random.randint(0, 10),
            "disliked": random.randint(0, 5),
            "replies": []
        })
    return reviews

# Số lượng tài khoản và đánh giá giả lập
num_accounts = 100
num_reviews = 1000

accounts = generate_fake_accounts(num_accounts)
reviews = generate_fake_reviews(num_reviews, num_accounts, interest_groups)
# In ra 5 đánh giá đầu tiên để kiểm tra
for review in reviews[:5]:
    print(review)

# Lưu dữ liệu vào file JSON
with open('fake_accounts.json', 'w', encoding='utf-8') as f:
    json.dump({"accounts": accounts}, f, ensure_ascii=False, indent=4)

with open('fake_reviews.json', 'w', encoding='utf-8') as f:
    json.dump({"reviews": reviews}, f, ensure_ascii=False, indent=4)
