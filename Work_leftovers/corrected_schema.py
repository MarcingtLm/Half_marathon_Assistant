from pandera import DataFrameSchema, Column, Check, Index, MultiIndex

schema = DataFrameSchema(
    columns={
        "Miejsce": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=15000, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=True,
            coerce=True,
            required=True,
            regex=False,
            description="Miejsce końcowe zawodnika w biegu",
            title="Miejsce",
        ),
        "Płeć": Column(
            dtype="object",
            checks=[
                Check.isin(["K", "M"]), 
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description="Płeć zawodnika: K - kobieta, M - mężczyzna",
            title="Płeć",
        ),
        "Płeć Miejsce": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=10000, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Miejsce w klasyfikacji płci",
            title="Płeć Miejsce",
        ),
        "Kategoria wiekowa": Column(
            dtype="object",
            checks=[
                # Wzorzec: K lub M + liczba (np. K20, M30, K40, M50, K60, M70)
                Check.str_matches(r"^[KM]\d{2}$"),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description="Kategoria wiekowa zawodnika (np. K30, M40)",
            title="Kategoria wiekowa",
        ),
        "Kategoria wiekowa Miejsce": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=3000, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Miejsce w kategorii wiekowej",
            title="Kategoria wiekowa Miejsce",
        ),
        "5 km Czas": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=600, raise_warning=False, ignore_na=True  
                ),
                Check.less_than_or_equal_to(
                    max_value=6000, raise_warning=False, ignore_na=True  
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Czas na 5 km w sekundach",
            title="5 km Czas",
        ),
        "5 km Miejsce Open": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=15000, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Miejsce open na 5 km",
            title="5 km Miejsce Open",
        ),
        "5 km Tempo": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=120.0, raise_warning=False, ignore_na=True  
                ),
                Check.less_than_or_equal_to(
                    max_value=1200.0, raise_warning=False, ignore_na=True  
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Tempo na 5 km w sekundach na kilometr",
            title="5 km Tempo",
        ),
        "10 km Czas": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1200, raise_warning=False, ignore_na=True  
                ),
                Check.less_than_or_equal_to(
                    max_value=12000, raise_warning=False, ignore_na=True 
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Czas na 10 km w sekundach",
            title="10 km Czas",
        ),
        "10 km Miejsce Open": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=15000, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Miejsce open na 10 km",
            title="10 km Miejsce Open",
        ),
        "10 km Tempo": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=120.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=1200.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Tempo na 10 km w sekundach na kilometr",
            title="10 km Tempo",
        ),
        "15 km Czas": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1800, raise_warning=False, ignore_na=True  
                ),
                Check.less_than_or_equal_to(
                    max_value=18000, raise_warning=False, ignore_na=True  
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Czas na 15 km w sekundach",
            title="15 km Czas",
        ),
        "15 km Miejsce Open": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=15000, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Miejsce open na 15 km",
            title="15 km Miejsce Open",
        ),
        "15 km Tempo": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=120.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=1200.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Tempo na 15 km w sekundach na kilometr",
            title="15 km Tempo",
        ),
        "20 km Czas": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=2400, raise_warning=False, ignore_na=True  
                ),
                Check.less_than_or_equal_to(
                    max_value=24000, raise_warning=False, ignore_na=True 
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Czas na 20 km w sekundach",
            title="20 km Czas",
        ),
        "20 km Miejsce Open": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=15000, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Miejsce open na 20 km",
            title="20 km Miejsce Open",
        ),
        "20 km Tempo": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=120.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=1200.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Tempo na 20 km w sekundach na kilometr",
            title="20 km Tempo",
        ),
        "Tempo Stabilność": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=-1.0, raise_warning=False, ignore_na=True 
                ),
                Check.less_than_or_equal_to(
                    max_value=1.0, raise_warning=False, ignore_na=True  
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Stabilność tempa (-1 do 1, gdzie 0 = idealne tempo)",
            title="Tempo Stabilność",
        ),
        "Czas": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=2520, raise_warning=False, ignore_na=True  
                ),
                Check.less_than_or_equal_to(
                    max_value=25200, raise_warning=False, ignore_na=True  
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Całkowity czas biegu w sekundach",
            title="Czas",
        ),
        "Tempo": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=120.0, raise_warning=False, ignore_na=True 
                ),
                Check.less_than_or_equal_to(
                    max_value=1200.0, raise_warning=False, ignore_na=True 
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Średnie tempo biegu w sekundach na kilometr",
            title="Tempo",
        ),
        "Wiek": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=16, raise_warning=False, ignore_na=True  
                ),
                Check.less_than_or_equal_to(
                    max_value=100, raise_warning=False, ignore_na=True  
                ),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
            regex=False,
            description="Wiek zawodnika w latach",
            title="Wiek",
        ),
    },
    checks=[
        # Sprawdzenie logicznej kolejności czasów - każdy kolejny dystans powinien mieć większy lub równy czas
        Check(
            lambda df: df["5 km Czas"].le(df["10 km Czas"]).all() 
                if "5 km Czas" in df.columns and "10 km Czas" in df.columns 
                else True,
            name="5km_przed_10km",
            error="Czas 5 km musi być mniejszy lub równy czasowi 10 km"
        ),
        Check(
            lambda df: df["10 km Czas"].le(df["15 km Czas"]).all() 
                if "10 km Czas" in df.columns and "15 km Czas" in df.columns 
                else True,
            name="10km_przed_15km",
            error="Czas 10 km musi być mniejszy lub równy czasowi 15 km"
        ),
        Check(
            lambda df: df["15 km Czas"].le(df["20 km Czas"]).all() 
                if "15 km Czas" in df.columns and "20 km Czas" in df.columns 
                else True,
            name="15km_przed_20km",
            error="Czas 15 km musi być mniejszy lub równy czasowi 20 km"
        ),
        Check(
            lambda df: df["20 km Czas"].le(df["Czas"]).all() 
                if "20 km Czas" in df.columns and "Czas" in df.columns 
                else True,
            name="20km_przed_mety",
            error="Czas 20 km musi być mniejszy lub równy czasowi końcowemu"
        ),
        Check(
            lambda df: df["Kategoria wiekowa"].str[0].eq(df["Płeć"]).all() 
                if "Kategoria wiekowa" in df.columns and "Płeć" in df.columns 
                else True,
            name="plec_kategoria_spojnosc",
            error="Pierwsza litera kategorii wiekowej musi odpowiadać płci"
        ),
        Check(
            lambda df: df["Płeć Miejsce"].le(df["Miejsce"]).all() 
                if "Płeć Miejsce" in df.columns and "Miejsce" in df.columns 
                else True,
            name="plec_miejsce_logika",
            error="Miejsce w klasyfikacji płci musi być <= miejsca ogólnego"
        ),
        Check(
            lambda df: df["Kategoria wiekowa Miejsce"].le(df["Płeć Miejsce"]).all() 
                if "Kategoria wiekowa Miejsce" in df.columns and "Płeć Miejsce" in df.columns 
                else True,
            name="kategoria_miejsce_logika",
            error="Miejsce w kategorii wiekowej musi być <= miejsca w płci"
        ),
    ],
    index=Index(
        dtype="int64",
        checks=[
            Check.greater_than_or_equal_to(
                min_value=0, raise_warning=False, ignore_na=True
            ),
        ],
        nullable=False,
        coerce=True,
        name=None,
        description="Indeks DataFrame",
        title=None,
    ),
    dtype=None,
    coerce=True,
    strict=False,
    name="HalfMarathonSchema",
    ordered=False,
    unique=None,
    report_duplicates="all",
    unique_column_names=True,
    add_missing_columns=False,
    title="Schemat danych półmaratonu",
    description="Schemat walidacji danych z półmaratonu wrocławskiego",
)
