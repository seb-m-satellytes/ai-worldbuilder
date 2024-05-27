Country size:
- max 10 000 000 sqkm
- min 300 sqkm

Country density:
- max 20 000 people/sqkm
- min 10 person/sqkm

Country population:
- max 500 000 000 people
- min 25 000 people

country_size < 1000 => regions_min, regions_max = 1, 1
country_size < 10_000 => regions_min, regions_max = 1, 3
country_size < 100_000 => regions_min, regions_max = 3, 12
country_size < 1_000_000 => regions_min, regions_max = 4, 24
regions_min, regions_max = 5, 36

metropolis 1_000_000+
city 100_000-1_000_000
town 10_000-100_000


world (o)
-
continent (o)
-
country (o)
├── region (o)
│   ├── metropolis (0)
│   │   ├── district (o)
│   │   │   └── neighborhood
│   │   ├── citizen
│   │   ├── infrastructure
│   │   │   ├── transportation
│   │   │   │   ├── highway
│   │   │   │   ├── railway
│   │   │   │   └── port
│   │   │   ├── utility
│   │   │   │   ├── power plant
│   │   │   │   ├── water treatment facility
│   │   │   │   └── waste management facility
│   │   │   └── landmark
│   │   │       ├── monument
│   │   │       ├── park
│   │   │       └── stadium
│   │   └── economy
│   │       ├── industry
│   │       │   ├── factory
│   │       │   └── warehouse
│   │       ├── commerce
│   │       │   ├── market
│   │       │   ├── shop
│   │       │   └── mall
│   │       └── financial institution
│   │           ├── bank
│   │           └── stock exchange
│   ├── city (o)
│   │   ├── district (o)
│   │   │   └── neighborhood
│   │   ├── citizen
│   │   ├── infrastructure
│   │   │   ├── transportation
│   │   │   │   ├── road
│   │   │   │   └── bridge
│   │   │   ├── utility
│   │   │   │   ├── power grid
│   │   │   │   └── water supply
│   │   │   └── landmark
│   │   │       ├── plaza
│   │   │       └── garden
│   │   └── economy
│   │       ├── industry
│   │       │   ├── workshop
│   │       │   └── guildhall
│   │       └── commerce
│   │           ├── marketplace
│   │           └── tavern
│   └── village
│       ├── citizen
│       ├── infrastructure
│       │   ├── transportation
│       │   │   └── trail
│       │   └── utility
│       │       ├── well
│       │       └── windmill
│       └── economy
│           ├── industry
│           │   ├── farm
│           │   └── mine
│           └── commerce
│               ├── general store
│               └── inn
└── governance
    ├── monarch
    ├── council
    │   ├── councilor
    │   └── advisor
    ├── court
    │   ├── judge
    │   └── lawyer
    └── military
        ├── army
        │   ├── soldier
        │   └── officer
        └── navy
            ├── sailor
            └── captain
