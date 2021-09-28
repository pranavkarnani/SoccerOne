from scrapy import Item, Field

class Player(Item):
    ID = Field()

    # General
    Name = Field()
    Natinality = Field()
    Overal = Field()
    Potential = Field()
    Height = Field()
    Weight = Field()
    PreferredFoot = Field()
    BirthDate = Field()
    Age = Field()
    PreferredPositions = Field()
    PlayerWorkRate = Field()
    WeakFoot = Field()
    SkillMoves = Field()
    Value = Field()
    Wage = Field()

    # Nation
    Nation = Field()
    Nation_Position = Field()
    Nation_KitNumber = Field()

    # Club
    Club = Field()
    Club_Position = Field()
    Club_KitNumber = Field()
    Club_JoinedClub = Field()
    Club_ContractLength = Field()

    # BallSkills
    BallControl = Field()
    Dribbling = Field()

    # Defence
    Marking = Field()
    SlideTackle = Field()
    StandTackle = Field()

    # Mental
    Aggression = Field()
    Reactions = Field()
    AttPosition = Field()
    Interceptions = Field()
    Vision = Field()
    Composure = Field()

    # Passing
    Crossing = Field()
    ShortPass = Field()
    LongPass = Field()

    # Physical
    Acceleration = Field()
    Stamina = Field()
    Strength = Field()
    Balance = Field()
    SprintSpeed = Field()
    Agility = Field()
    Jumping = Field()

    # Shooting
    Heading = Field()
    ShotPower = Field()
    Finishing = Field()
    LongShots = Field()
    Curve = Field()
    FKAcc = Field()
    Penalties = Field()
    Volleys = Field()

    # Goalkeeper
    GKPositioning = Field()
    GKDiving = Field()
    GKHandling = Field()
    GKKicking = Field()
    GKReflexes = Field()

    Traits = Field()
    Specialities = Field()