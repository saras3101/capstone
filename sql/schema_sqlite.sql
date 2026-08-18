CREATE TABLE IF NOT EXISTS iucr (
    iucr_code INTEGER PRIMARY KEY,
    primary_type TEXT,
    description TEXT,
    index_code TEXT
);

CREATE TABLE IF NOT EXISTS police_beat_info (
    beat_num INTEGER PRIMARY KEY,
    district INTEGER,
    sector INTEGER,
    beat INTEGER
);

CREATE TABLE IF NOT EXISTS district_ps_info (
    district_code INTEGER PRIMARY KEY,
    district_name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    website TEXT,
    phone TEXT,
    fax TEXT,
    tty TEXT,
    x_coordinate REAL,
    y_coordinate REAL,
    latitude REAL,
    longitude REAL,
    location TEXT
);

CREATE TABLE IF NOT EXISTS ward_office (
    ward_no INTEGER PRIMARY KEY,
    alderman TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zipcode TEXT,
    ward_phone TEXT,
    ward_fax TEXT,
    email TEXT,
    website TEXT,
    location TEXT,
    city_hall_address TEXT,
    city_hall_city TEXT,
    city_hall_state TEXT,
    city_hall_zipcode TEXT,
    city_hall_phone TEXT
);

CREATE TABLE IF NOT EXISTS city_community (
    community_code INTEGER PRIMARY KEY,
    community_name TEXT,
    population INTEGER,
    area_sqmile REAL,
    area_sqkm REAL,
    density_per_sqmi REAL,
    density_per_sqkm REAL
);

CREATE TABLE IF NOT EXISTS chicago_crime (
    id INTEGER PRIMARY KEY,
    case_number TEXT,
    date TEXT,
    block TEXT,
    iucr_code INTEGER,
    primary_type TEXT,
    description TEXT,
    location_desc TEXT,
    arrest INTEGER,
    domestic INTEGER,
    beat_num INTEGER,
    district_code INTEGER,
    ward_no INTEGER,
    community_code INTEGER,
    fbi_code TEXT,
    x_coordinate REAL,
    y_coordinate REAL,
    year INTEGER,
    date_of_update TEXT,
    latitude REAL,
    longitude REAL,
    location TEXT,
    crime_month INTEGER,
    crime_dayofweek TEXT,
    FOREIGN KEY (iucr_code) REFERENCES iucr(iucr_code),
    FOREIGN KEY (beat_num) REFERENCES police_beat_info(beat_num),
    FOREIGN KEY (district_code) REFERENCES district_ps_info(district_code),
    FOREIGN KEY (ward_no) REFERENCES ward_office(ward_no),
    FOREIGN KEY (community_code) REFERENCES city_community(community_code)
);