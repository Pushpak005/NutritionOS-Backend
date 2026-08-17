TODAY_FILTER = """

DATE(

    COALESCE(

        m.consumed_at,

        m.created_at

    )

)=CURRENT_DATE

"""