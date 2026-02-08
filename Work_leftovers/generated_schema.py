from pandera import DataFrameSchema, Column, Check, Index, MultiIndex

schema = DataFrameSchema(
    columns={
        "Miejsce": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=10302.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Płeć": Column(
            dtype="object",
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Płeć Miejsce": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=7240.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Kategoria wiekowa": Column(
            dtype="object",
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Kategoria wiekowa Miejsce": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=2388.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Rocznik": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1944.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=2006.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "5 km Czas": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=906.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=3014.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "5 km Miejsce Open": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=2.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=10353.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "5 km Tempo": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=181.2, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=727.87, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "10 km Czas": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1782.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=6208.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "10 km Miejsce Open": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=10330.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "10 km Tempo": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=175.2, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=680.8, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "15 km Czas": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=2707.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=9249.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "15 km Miejsce Open": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=10305.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "15 km Tempo": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=185.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=672.8, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "20 km Czas": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=3633.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=12082.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "20 km Miejsce Open": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=1.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=10306.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "20 km Tempo": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=185.2, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=713.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Tempo Stabilność": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=-0.844026, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=0.812362, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Czas": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=3843.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=12754.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Tempo": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=182.17587105949278,
                    raise_warning=False,
                    ignore_na=True,
                ),
                Check.less_than_or_equal_to(
                    max_value=604.5982460298651,
                    raise_warning=False,
                    ignore_na=True,
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Wiek": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=18.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=80.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
    },
    checks=None,
    index=Index(
        dtype="int64",
        checks=[
            Check.greater_than_or_equal_to(
                min_value=0.0, raise_warning=False, ignore_na=True
            ),
            Check.less_than_or_equal_to(
                max_value=10299.0, raise_warning=False, ignore_na=True
            ),
        ],
        nullable=False,
        coerce=False,
        name=None,
        description=None,
        title=None,
    ),
    dtype=None,
    coerce=True,
    strict=False,
    name=None,
    ordered=False,
    unique=None,
    report_duplicates="all",
    unique_column_names=False,
    add_missing_columns=False,
    title=None,
    description=None,
)
