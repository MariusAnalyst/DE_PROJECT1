with staging as (

    select * from {{ ref('stg_mental_health') }}

),

final as (

    select
        -- Dimensions
        Timestamp as created_at,
        Gender as gender,
        Country as country,
        Occupation as occupation,
        
        -- Employment Status
        self_employed,
        
        -- Mental Health Indicators
        family_history,
        treatment,
        Days_Indoors as days_indoors,
        Growing_Stress as growing_stress,
        Changes_Habits as changes_habits,
        Mental_Health_History as mental_health_history,
        Mood_Swings as mood_swings,
        Coping_Struggles as coping_struggles,
        Work_Interest as work_interest,
        Social_Weakness as social_weakness,
        mental_health_interview,
        care_options

    from staging

)

select * from final
