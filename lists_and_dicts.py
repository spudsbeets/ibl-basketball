regions = ['West Coast USA', 'Midwest USA', 'East Coast USA', 'South USA', 'Canada',
           'South America', 'Europe', 'Asia', 'Africa', 'Australia']

positions = ['PG', 'SG', 'SF', 'PF', 'C']

names = {
    # 100 Each
    'America': {
        'First': ["Liam", "Noah", "Oliver", "Elijah", "James", "Benjamin", "Lucas", "Henry",
                "Alexander", "William", "Jack", "Theodore", "Levi", "Daniel", "Logan",
                "Jackson", "Sebastian", "Mateo", "Samuel", "David", "Joseph", "Carter",
                "Owen", "Wyatt", "John", "Isaac", "Luke", "Julian", "Grayson", "Caleb",
                "Ezra", "Gabriel", "Hudson", "Lincoln", "Thomas", "Nathan", "Maverick",
                "Elias", "Anthony", "Dylan", "Asher", "Charles", "Josiah", "Christian",
                "Andrew", "Leo", "Ryan", "Everett", "Nolan", "Aaron", "Miles", "Eli",
                "Adam", "Connor", "Dominic", "Ian", "Austin", "Brayden", "Jason", "Xavier",
                "Jaxon", "Micah", "Camden", "Wesley", "Beau", "Chase", "Cole", "Zachary",
                "Nathaniel", "Hunter", "Jonathan", "Roman", "Adrian", "Easton", "Max",
                "Silas", "Ezekiel", "Vincent", "Brooks", "Bentley", "Kayden", "George",
                "Kaiden", "Bryson", "Sawyer", "Harrison", "Tyler", "Axel", "Diego",
                "Braxton", "Declan", "Ivan", "Maxwell", "Jayden", "Jude", "Emmett",
                "Malachi", "Kingston", "Kaden", "Gavin", "Zayden", "Tristan"],
        'Last': ["Smith", "Johnson", "Brown", "Taylor", "Anderson", "Thomas", "Jackson",
                "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
                "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young",
                "King", "Wright", "Scott", "Green", "Baker", "Adams", "Nelson", "Hill",
                "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans", "Turner",
                "Parker", "Collins", "Edwards", "Stewart", "Morris", "Nguyen", "Murphy",
                "Rogers", "Cook", "Morgan", "Peterson", "Reed", "Bailey", "Bell", "Gomez",
                "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres", "Flores",
                "Wood", "Griffin", "Russell", "Diaz", "Hayes", "Butler", "Simmons",
                "Foster", "Gonzalez", "Bryant", "Alexander", "Russell", "Hughes", "Myers",
                "Long", "Graham", "Bennett", "Gray", "James", "Watson", "Brooks",
                "Kelly", "Sanders", "Price", "Bennett", "Reyes", "Powell", "Jenkins",
                "Perry", "Patterson", "Hughes", "Coleman", "Henderson", "Cole", "Sullivan",
                "Hart", "Stephens", "Murray", "Freeman", "Black", "Marshall"]
    },
    # 60 Each for rest
    'Canada': {
        'First': ["Liam", "Noah", "Jackson", "Lucas", "Benjamin", "Oliver", "William", "Logan",
                "James", "Jacob", "Nathan", "Ethan", "Mason", "Gabriel", "Samuel", "Alexandre",
                "Owen", "Caleb", "Matthew", "Maxime", "Charles", "Julien", "Xavier", "Étienne",
                "Thomas", "Gabriel", "Raphaël", "Simon", "David", "Léo", "Maxwell", "Zachary",
                "Connor", "Tyler", "Daniel", "Anthony", "Adrian", "Maxence", "Jean", "Frédéric",
                "Nathaniel", "Mark", "Patrick", "Sebastien", "Vincent", "Joseph", "Émile",
                "Julien", "Cameron", "Brandon", "Logan", "Dylan", "Jaden", "Evan", "Isaac",
                "Olivier", "Louis", "Nolan", "Cédric", "Felix", "Dominic"],
        'Last': ["Smith", "Brown", "Wilson", "Taylor", "Johnson", "White", "Martin", "MacDonald",
                "Anderson", "Thompson", "Robinson", "Campbell", "Miller", "Clark", "Wright",
                "Scott", "Young", "Evans", "Hall", "Turner", "Côté", "Tremblay", "Gagnon",
                "Lavoie", "Roy", "Bouchard", "Girard", "Fortin", "Pelletier", "Lemieux",
                "Bergeron", "Dion", "Caron", "Lemay", "Morin", "Blais", "Simard", "Cloutier",
                "Gauthier", "Paquette", "Lacroix", "Ouellet", "Charron", "Allard", "Cyr",
                "Boucher", "Landry", "Beaulieu", "Desjardins", "Boisvert", "Marchand",
                "Leblanc", "Picard", "Perreault", "Parent", "Levesque", "Roy", "Benoit",
                "Dufour", "Richard", "Gaudreau", "Blanchette", "Boudreau"]
    },
    'South America': {
        'First': ["Mateo", "Santiago", "Matías", "Thiago", "Benjamín", "Luciano", "Joaquín",
                "Gabriel", "Juan", "Tomás", "Nicolás", "Andrés", "Pedro", "Diego", "Lucas",
                "Martín", "Felipe", "Emiliano", "Facundo", "Bruno", "Agustín", "Franco",
                "Rodrigo", "Axel", "Gael", "Alan", "Maximiliano", "Samuel", "Antonio",
                "Eduardo", "Enzo", "Luis", "Adrián", "Cristian", "Esteban", "Alejandro",
                "Alonso", "Carlos", "Fernando", "Rafael", "Miguel", "Manuel", "José",
                "Ricardo", "Ángel", "Hugo", "Iván", "Raúl", "Mauricio", "Danilo", "Gustavo",
                "Otávio", "Henrique", "Caio", "Leonardo", "Vinícius", "João", "Ruan", "Heitor",
                "Arthur", "Anderson"],
        'Last': ["González", "Rodríguez", "Gómez", "Fernández", "López", "Martínez", "Pérez",
                "Sánchez", "Ramírez", "Torres", "Flores", "Vargas", "Díaz", "Castro", "Rojas",
                "Morales", "Herrera", "Mendoza", "Jiménez", "Silva", "Alvarez", "Romero",
                "Ortega", "Navarro", "Delgado", "Cruz", "Reyes", "Chávez", "Salazar", "Medina",
                "Fuentes", "Suárez", "Aguilar", "Vega", "Campos", "Cortés", "Carrillo",
                "Bravo", "Arias", "Peña", "Pacheco", "Ibarra", "Montoya", "Acosta", "Mora",
                "Espinoza", "Quiroz", "Palacios", "Cárdenas", "Tapia", "Correa", "Barrios",
                "Castillo", "Soto", "Almeida", "Souza", "Oliveira", "Costa", "Lima", "Barbosa"]
    },
    'Europe': {
        'First': ["Luca", "Matteo", "Leon", "Sebastian", "Niko", "Julian", "Emil", "Andreas",
                "Alexandre", "Hugo", "Maxim", "Tomas", "Felix", "Jan", "Milan", "Dominik",
                "Oskar", "Erik", "Theo", "Raphael", "Jakub", "Adam", "Elias", "Lars",
                "Daniel", "Samuel", "Nils", "Johan", "Ruben", "Henrik", "Anton", "Kasper",
                "Marc", "Alban", "Victor", "Kristian", "Bastian", "Sven", "Oscar", "Simon",
                "Gabriel", "Ivan", "Pavel", "Stefan", "Rafael", "Martin", "Niklas", "George",
                "Lukasz", "Francesco", "Ignacio", "Arne", "Eduard", "Marek", "Filip",
                "Andrei", "Kristof", "Pascal", "Dimitri", "Jens"],
        'Last': ["Müller", "Schmidt", "Schneider", "Fischer", "Weber",
                "Dubois", "Lefevre", "Moreau", "Laurent", "Simon",
                "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi",
                "Smirnov", "Ivanov", "Kuznetsov", "Popov", "Volkov",
                "Nowak", "Kowalski", "Wisniewski", "Dabrowski", "Kaminski",
                "Garcia", "Martinez", "Lopez", "Sanchez", "Gonzalez",
                "Silva", "Ferreira", "Costa", "Oliveira", "Sousa",
                "Johansson", "Andersson", "Karlsson", "Nilsson", "Eriksson",
                "Jensen", "Nielsen", "Hansen", "Larsen", "Madsen",
                "Novak", "Svoboda", "Dvořák", "Procházka", "Kučera",
                "Popa", "Ionescu", "Stan", "Dumitru", "Stoica",
                "Petrov", "Dimitrov", "Ivanov", "Georgiev", "Nikolov"]
    },
    'Asia': {
        'First': ["Wei", "Xiao", "Lei", "Hao", "Jun", "Bo", "Tian", "Chen", "Ming", "Jian",
                "Haruki", "Kaito", "Ren", "Souta", "Takumi", "Yuki", "Riku", "Daiki", "Hiroshi", "Takeshi",
                "Joon", "Minho", "Hyun", "Jihoon", "Sung", "Taeyang", "Dae", "Jisoo", "Seojun", "Young",
                "Arjun", "Rahul", "Ravi", "Amit", "Vikram", "Kunal", "Rohan", "Nikhil", "Sanjay", "Dev",
                "Ali", "Omar", "Hassan", "Ahmad", "Zaid", "Imran", "Farhan", "Naveed", "Salman", "Ayaan",
                "Minh", "Thanh", "Phuc", "Kiet", "Somchai", "Aditya", "Bayani", "Andres", "Jose", "Marco"],
        'Last': ["Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou",
                "Kim", "Lee", "Park", "Choi", "Jung", "Kang", "Cho", "Yoon", "Jang", "Lim",
                "Singh", "Kumar", "Sharma", "Gupta", "Patel", "Das", "Reddy", "Mehta", "Chowdhury", "Malhotra",
                "Nguyen", "Tran", "Le", "Pham", "Hoang", "Bui", "Dang", "Vu", "Pham", "Do",
                "Tan", "Teo", "Lim", "Ng", "Ong", "Chua", "Santos", "Dela Cruz", "Garcia", "Reyes",
                "Khan", "Hussain", "Aziz", "Mirza", "Farooq", "Iqbal", "Malik", "Shaikh", "Rizvi", "Qureshi"]
    },
    'Africa': {
        'First': ["Kwame", "Kofi", "Ade", "Chike", "Jabari", "Temba", "Thabo", "Nuru", "Amari", "Sekou",
                "Mandela", "Obasi", "Zuberi", "Sefu", "Lamine", "Khalil", "Biko", "Ayo", "Faraji", "Juma",
                "Amadou", "Cheikh", "Babacar", "Omar", "Abdul", "Ibrahim", "Malik", "Femi", "Tariq", "Hassan",
                "Kelechi", "Chinedu", "Emeka", "Olu", "Ngozi", "Tendai", "Simba", "Aziz", "Ishmael", "Kamau",
                "Jelani", "Kwesi", "Zola", "Omari", "Bakari", "Mosi", "Nia", "Zain", "Azubuike", "Ekon",
                "Lutalo", "Sekani", "Rashid", "Said", "Tawanda", "Zuri", "Kamari", "Oba", "Dumi", "Chuma"],
        'Last': ["Okeke", "Diallo", "Mensah", "Ndlovu", "Abebe", "Kamau", "Traoré", "Chukwu",
                "Mbeki", "Kone", "Adams", "Jalloh", "Balogun", "Osei", "Toure", "Nkosi",
                "Adebayo", "Bello", "Fofana", "Sow", "Dlamini", "Gyamfi", "Ncube", "Mohammed",
                "Ibrahim", "Banda", "Chibueze", "Onyango", "Mwangi", "Okoro", "Amadou",
                "Sekou", "Acheampong", "Diop", "Kamara", "Omar", "Kaggwa", "Mathebula",
                "Ngugi", "Okafor", "Sesay", "Abdullahi", "Achieng", "Tshabalala", "Bamgbose",
                "Eze", "Kouyaté", "Moyo", "Kone", "Mansaray", "Maphosa", "Ntuli", "Otieno",
                "Senghor", "Umar", "Yeboah", "Zuma", "Chima", "Dada", "Etienne"]
    },
    'Australia': {
        'First': ["Oliver", "Jack", "William", "Noah", "Thomas", "James", "Lachlan", "Ethan",
                "Lucas", "Mason", "Alexander", "Henry", "Charlie", "Leo", "Max", "Samuel",
                "Jacob", "Harrison", "Hunter", "Isaac", "Cooper", "Logan", "Blake", "Zachary",
                "Tyler", "Joshua", "Finn", "Caleb", "Connor", "Eli", "Archie", "Jaxon",
                "Jake", "George", "Hudson", "Riley", "Jayden", "Nicholas", "Sebastian",
                "Matthew", "David", "Daniel", "Cameron", "Kai", "Marcus", "Patrick", "Ryan",
                "Toby", "Owen", "Mitchell", "Thomas", "Liam", "Brayden", "Charles", "Jordan",
                "Elliott", "Nathan", "Zane", "Jude", "Lincoln", "Angus"],
        'Last': ["Smith", "Jones", "Williams", "Brown", "Wilson", "Taylor", "Johnson", "White",
                "Martin", "Anderson", "Thomas", "Jackson", "Robinson", "Wright", "Walker",
                "Thompson", "Harris", "Lewis", "Scott", "Miller", "Clark", "Young", "King",
                "Hill", "Green", "Adams", "Baker", "Nelson", "Carter", "Mitchell", "Perez",
                "Roberts", "Campbell", "Evans", "Collins", "Edwards", "Stewart", "Morris",
                "Murphy", "Cook", "Rogers", "Reed", "Cooke", "Morgan", "Bell", "Bailey",
                "Cooper", "Richardson", "Kelly", "Howard", "Ward", "Cox", "Ward", "Ward",
                "Foster", "Gray", "James", "Watson", "Price", "Brooks"]
    }
}

heights = {
    'PG': {
        'low': 70,
        'high': 82
    },
    'SG': {
        'low': 70,
        'high': 82
    },
    'SF': {
        'low': 75,
        'high': 84
    },
    'PF': {
        'low': 75,
        'high': 84
    },
    'C': {
        'low': 78,
        'high': 88
    }
}

weights = {
    'PG': {
        'low': 170,
        'high': 220
    },
    'SG': {
        'low': 170,
        'high': 220
    },
    'SF': {
        'low': 200,
        'high': 260
    },
    'PF': {
        'low': 200,
        'high': 260
    },
    'C': {
        'low': 220,
        'high': 290
    }
}

intangibles = ['Low', 'Somewhat Low', 'Average', 'Somewhat High', 'High']

cities = {
    'West Coast USA': ["Los Angeles", "San Francisco", "Seattle", "San Diego", "Portland"],
    'Midwest USA': ["Chicago", "Detroit", "Minneapolis", "Cleveland", "St. Louis"],
    'East Coast USA': ["New York City", "Boston", "Philadelphia", "Washington, D.C.", "Baltimore"],
    'South USA': ["Atlanta", "Miami", "Houston", "Dallas", "New Orleans"],
    'Canada': ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
    'South America': ["São Paulo", "Buenos Aires", "Lima", "Bogotá", "Santiago"],
    'Europe': ["London", "Paris", "Berlin", "Rome", "Madrid"],
    'Asia': ["Tokyo", "Shanghai", "Mumbai", "Seoul", "Bangkok"],
    'Africa': ["Lagos", "Cairo", "Nairobi", "Johannesburg", "Addis Ababa"],
    'Australia': ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"]
}

nicknames = ["Thunder", "Titans", "Wolves", "Falcons", "Storm", "Dragons", "Raiders", "Vipers",
             "Crusaders", "Hawks", "Panthers", "Gladiators", "Warriors", "Cyclones", "Sharks",
             "Bulldogs", "Grizzlies", "Knights", "Raptors", "Pirates", "Bison", "Tornadoes",
             "Cobras", "Outlaws", "Phoenix", "Eagles", "Jets", "Samurais", "Spartans", "Tigers",
             "Rhinos", "Hornets", "Blizzards", "Commanders", "Patriots", "Lions", "Titans",
             "Scorpions", "Rebels", "Barracudas", "Gorillas", "Inferno", "Mavericks", "Mustangs",
             "Sabers", "Bearcats", "Sentinels", "Crushers", "Avalanche", "Pythons"]

color_schemes = ["blue/white", "red/black", "green/white", "purple/gold", "black/silver", "orange/navy",
                 "maroon/white", "navy/gold", "teal/black", "crimson/cream", "gray/blue", "black/red",
                 "royal blue/yellow", "forest green/gold", "sky blue/white", "burgundy/gray", "red/white",
                 "blue/gold", "orange/white", "brown/yellow", "charcoal/teal", "black/gold", "green/silver",
                 "navy/white", "turquoise/purple", "silver/maroon", "cyan/black", "olive/cream", "indigo/gray",
                 "pink/black", "yellow/black", "red/gray"]