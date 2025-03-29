"""import enum
from models import MembershipTypeEnum,GenderEnum


# Membership durations (Leap-Year Proof using weekly-based logic)
MEMBERSHIP_DURATIONS = {
    MembershipTypeEnum.TRIAL: 7,        # 1 week
    MembershipTypeEnum.MONTHLY: 28,     # 4 weeks
    MembershipTypeEnum.QUARTERLY: 84,   # 12 weeks
    MembershipTypeEnum.HALFYEARLY: 168, # 24 weeks
    MembershipTypeEnum.ANNUALLY: 336    # 48 weeks
}

# Discount rates
DISCOUNT_RATES = {
    MembershipTypeEnum.TRIAL: 1,        # Free trial (100% off)
    MembershipTypeEnum.MONTHLY: 0.1,    
    MembershipTypeEnum.QUARTERLY: 0.2,  
    MembershipTypeEnum.HALFYEARLY: 0.3, 
    MembershipTypeEnum.ANNUALLY: 0.4    
}

# Discount calculation
def calculate_discounted_price(base_price: float, membership_type: MembershipTypeEnum,gender) -> float:
    discount = DISCOUNT_RATES.get(membership_type,0)

    if gender == GenderEnum.FEMALE:
        discount += 0.05 # To Promoto Female Participation In Gym

    return base_price * (1 - discount)    """
