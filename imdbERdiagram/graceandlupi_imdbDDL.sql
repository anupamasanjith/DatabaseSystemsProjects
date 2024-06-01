-- create new table title.akas with references to title.basics
-- one to many relationship
create table public."title.akas"
(
    "titleID"         varchar not null
        constraint "title.akas_pk"
            primary key
        constraint "title.akas_title.basics_tconst_fk"
            references public."title.basics",
    ordering          integer,
    title             varchar not null,
    region            varchar,
    language          varchar not null,
    "isOriginalTitle" bit
);

alter table public."title.akas"
    owner to asanj19;

grant delete, insert, select, update on public."title.akas" to gkbrid20;


-- create new table akas.types with references to title.akas
-- one to many relationship
create table public."akas.types"
(
    "titleID" varchar not null
        constraint "akas.types_pk"
            primary key
        constraint "akas.types_title.akas_titleID_fk"
            references public."title.akas",
    type      varchar
);

alter table public."akas.types"
    owner to asanj19;

grant delete, insert, select, update on public."akas.types" to gkbrid20;

-- create new table akas.attributes with references to title.akas
-- one to many relationship
create table public."akas.attributes"
(
    "titleID" varchar not null
        constraint "akas.attributes_pk"
            primary key
        constraint "akas.attributes_title.akas_titleID_fk"
            references public."title.akas",
    attribute varchar
);

alter table public."akas.attributes"
    owner to asanj19;

grant delete, insert, select, update on public."akas.attributes" to gkbrid20;


-- create new table title.types with primary kwy tconst

create table public."title.basics" (
  tconst character varying primary key not null,
  "titleType" character varying,
  "primaryTitle" character varying,
  "orginalTitle" character varying,
  "isAdult" bit(1),
  "startYear" integer,
  "endYear" integer,
  "runtimeMinutes" integer
);

-- create new table basics.genre with references to title.basics
-- one to many relationship
create table public."basics.genre"
(
    tconst varchar not null
        constraint "basics.genre_pk"
            primary key
        constraint "basics.genre_title.basics_tconst_fk"
            references public."title.basics",
    genre  varchar
);

alter table public."basics.genre"
    owner to asanj19;

grant delete, insert, select, update on public."basics.genre" to gkbrid20;

-- create new table title.ratings with references to title.basics
-- one to one relationship
create table public."title.ratings" (
  tconst character varying primary key not null,
  "averageRating" integer,
  "numVotes" integer,
  foreign key (tconst) references public."title.basics" (tconst)
  match simple on update no action on delete no action
);

-- create new table title.episode with references to title.basics
-- one to many relationship
create table public."title.episode"
(
    tconst          varchar not null
        constraint "title.episode_pk"
            primary key,
    "parentTconst"  varchar
        constraint "title.episode_title.basics_tconst_fk"
            references public."title.basics",
    "seasonNumber"  integer,
    "episodeNumber" integer
);

alter table public."title.episode"
    owner to asanj19;

grant delete, insert, select, update on public."title.episode" to gkbrid20;

-- create new table name.basics with primary key nconst

create table public."name.basics"
(
    nconst        varchar not null
        constraint "name.basics_pk"
            primary key,
    "primaryName" varchar,
    "birthYear"   integer,
    "deathYear"   integer
);

alter table public."name.basics"
    owner to asanj19;

grant delete, insert, select, update on public."name.basics" to gkbrid20;

-- create new table name.knownForTitles with references to name.basics
-- one to many relationship

create table public."name.knownForTitles"
(
    nconst           varchar not null
        constraint "name.knownForTitles_pk"
            primary key
        constraint "name.knownForTitles_name.basics_nconst_fk"
            references public."name.basics",
    "knownForTitles" varchar
);

alter table public."name.knownForTitles"
    owner to asanj19;

grant delete, insert, select, update on public."name.knownForTitles" to gkbrid20;

-- create new table name.primaryProfession with references to name.basics
-- one to many relationship

create table public."name.primaryProfession"
(
    nconst              varchar not null
        constraint "name.primaryProfession_pk"
            primary key
        constraint "name.primaryProfession_name.basics_nconst_fk"
            references public."name.basics",
    "primaryProfession" varchar
);

alter table public."name.primaryProfession"
    owner to asanj19;

grant delete, insert, select, update on public."name.primaryProfession" to gkbrid20;

-- create new table title.principles with references to name.basics and title.basics
-- one to many relationship for both references
create table public."title.principles"
(
    tconst     varchar not null
        constraint "title.principles_pk"
            primary key
        constraint "title.principles_title.basics_tconst_fk"
            references public."title.basics",
    ordering   integer,
    category   varchar,
    job        varchar,
    characters varchar,
    nconst     varchar
        constraint "title.principles_name.basics_nconst_fk"
            references public."name.basics"
);

alter table public."title.principles"
    owner to asanj19;

grant delete, insert, select, update on public."title.principles" to gkbrid20;

-- create new table title.crew with references to title.basics
-- one to many relationship

create table public."title.crew"
(
    tconst varchar not null
        constraint "title.crew_pk"
            primary key
        constraint "title.crew_title.basics_tconst_fk"
            references public."title.basics"
);

alter table public."title.crew"
    owner to asanj19;

grant delete, insert, select, update on public."title.crew" to gkbrid20;

-- create new table crew.directors with references to name.basics and title.crew
-- one to many relationship for reference to title.crew
-- one to one relationship for reference to name.basics

create table public."crew.directors"
(
    tconst   varchar not null
        constraint "crew.directors_pk"
            primary key
        constraint "crew.directors_title.crew_tconst_fk"
            references public."title.crew",
    director varchar not null
        constraint "crew.directors_name.basics_nconst_fk"
            references public."name.basics"
);

alter table public."crew.directors"
    owner to asanj19;

grant delete, insert, select, update on public."crew.directors" to gkbrid20;

--- create new table crew.writers with references to name.basics and title.crew
-- one to many relationship for both references

create table public."crew.writers"
(
    tconst varchar not null
        constraint "crew.writers_pk"
            primary key
        constraint "crew.writers_title.crew_tconst_fk"
            references public."title.crew",
    writer varchar
        constraint "crew.writers_name.basics_nconst_fk"
            references public."name.basics"
);

alter table public."crew.writers"
    owner to asanj19;

grant delete, insert, select, update on public."crew.writers" to gkbrid20;





























