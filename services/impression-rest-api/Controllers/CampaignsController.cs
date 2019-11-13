using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Threading.Tasks;
using Dapper;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using MySql.Data.MySqlClient;

namespace impression_rest_api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class CampaignsController : ControllerBase
    {
        private readonly ILogger<CampaignsController> _logger;
        private readonly IDbConnection _con;

        public CampaignsController(ILogger<CampaignsController> logger, MySqlConnection connection)
        {
            _logger = logger;
            _con = connection;

            _logger.LogInformation("Campaigns controller resolved...");
        }

        /// <summary>
        /// 
        /// </summary>
        [HttpGet("ping")]
        public async Task<ActionResult<Question1>> Ping()
        {
             _logger.LogInformation("Ping action resolved...");

            return Ok("OK");
        }

        /// <summary>
        /// 
        /// </summary>
        [HttpGet("timeseries")]
        public async Task<ActionResult<Question1>> GetQuestion1()
        {
            _logger.LogInformation("Q1 action resolved...");

            var data = await _con.QueryAsync<Question1>(@"
                SELECT
                    date AS Date
                    ,id_campaign AS CampaignId
                    ,SUM(impressions) AS Impressions
                FROM agg_daily
                GROUP BY date, id_campaign
                ORDER BY date
            ");

            return Ok(data);
        }

        /// <summary>
        /// 
        /// </summary>
        [HttpGet("{id}/ads")]
        public async Task<ActionResult<Question2>> GetQuestion2(uint id)
        {
            _logger.LogInformation("Q2 action resolved...");

            var data = await _con.QueryAsync<Question2>(@"
                SELECT
                    CONCAT(id_campaign, '-', id_ad) AS AdId
                    ,SUM(impressions) AS Impressions
                    ,SUM(interactions) AS Interactions
                    ,SUM(swipes) AS Swipes
                FROM agg_daily
                WHERE id_campaign = @id
                GROUP BY id_campaign, id_ad
                ORDER BY id_campaign, id_ad
            ", new { id });

            return Ok(data);
        }

        /// <summary>
        /// 
        /// </summary>
        [HttpGet("ads/lastweek")]
        public async Task<ActionResult<Question3>> GetQuestion3()
        {
            _logger.LogInformation("Q3 action resolved...");

            var data = await _con.QueryAsync<Question3>(@"
                SELECT
					date AS Date
                    ,CONCAT(id_campaign, '-', id_ad) AS AdId
                    ,impressions AS Impressions
                    ,uniqueUsers AS UniqueUsers
                FROM agg_daily
                WHERE date >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK)
                ORDER BY date
            ");

            return Ok(data);
        }
    }


    public class Question1
    {
        public DateTime Date { get; set; }

        public string CampaignId { get; set; }

        public long Impressions { get; set; }
    }

    public class Question2
    {
        public string AdId { get; set; }

        public long Impressions { get; set; }

        public long Interactions { get; set; }

        public long Swipes { get; set; }
    }

    public class Question3
    {
        public DateTime Date { get; set; }

        public string AdId { get; set; }

        public long Impressions { get; set; }

        public long UniqueUsers { get; set; }
    }
}
