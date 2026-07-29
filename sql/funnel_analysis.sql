DROP VIEW IF EXISTS session_funnel;
CREATE VIEW session_funnel AS
SELECT
    SessionID,
    MAX(UserID)         AS UserID,
    MAX(DeviceType)      AS DeviceType,
    MAX(Country)         AS Country,
    MAX(ReferralSource)  AS ReferralSource,
    MAX(Purchased)       AS Purchased,
    MAX(CASE PageType
            WHEN 'home'         THEN 0
            WHEN 'product_page' THEN 1
            WHEN 'cart'         THEN 2
            WHEN 'checkout'     THEN 3
            WHEN 'confirmation' THEN 4 END)      AS max_step_order
FROM raw_events
GROUP BY SessionID;

WITH steps(step_order, step) AS (
    VALUES (0,'home'), (1,'product_page'), (2,'cart'), (3,'checkout'), (4,'confirmation')
),
funnel_counts AS (
    SELECT s.step_order, s.step, COUNT(sf.SessionID) AS sessions
    FROM steps s
    LEFT JOIN session_funnel sf ON sf.max_step_order >= s.step_order
    GROUP BY s.step_order, s.step
)
SELECT
    step_order, step, sessions,
    ROUND(100.0 * sessions / FIRST_VALUE(sessions) OVER (ORDER BY step_order), 2) AS pct_of_home,
    ROUND(100.0 * sessions / LAG(sessions)         OVER (ORDER BY step_order), 2) AS step_over_step_pct
FROM funnel_counts
ORDER BY step_order;