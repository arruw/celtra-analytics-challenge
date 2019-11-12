using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Threading.Tasks;
using Dapper;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
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
        }

        [HttpGet]
        public async Task<ActionResult<dynamic>> Get()
        {
            var data = await _con.QueryAsync("SELECT * FROM agg_daily");
            return Ok(data);
        }

        /// <summary>
        /// Campaigns timeseries data
        /// </summary>
        /// <param name="m">Selected metrics, override default metrics</param>
        [HttpGet("ts/{m?}")]
        public async Task<ActionResult<AggDaily>> Get(string m = "campaignName,impressions,interactions,clicks,uniqueUsers")
        {
            return await Get(null, m);
        }

        /// <summary>
        /// Campaign timeseries data
        /// </summary>
        /// <param name="id">Campaign id</param>
        /// <param name="m">Selected metrics, override default metrics</param>
        [HttpGet("ts/{id:int}/{m?}")]
        public async Task<ActionResult<AggDaily>> Get(uint? id, string m = "campaignName,impressions,interactions,clicks,uniqueUsers")
        {
            var mc = m.Split(',');

            var query = @$"SELECT * FROM agg_daily";
            var data = await _con.QueryAsync(query);

            // if(id.HasValue)
            //     query = query.Where(x => x.CampaignId == id);

            // var data = await query
            //     .GroupBy(x => x.Date)
            //     .OrderBy(x => x.Key)
            //     .ToListAsync();

            // var d = data.Select(x => new AggDaily
            //     {
            //         Date = x.First().Date,
            //         CampaignId = x.First().CampaignId,
                    
            //         CampaignName =  mc.Contains("campaignName") ? x.First().CampaignName        : null,
            //         Impressions =   mc.Contains("impressions") ? x.Sum(y => y.Impressions)      : null,
            //         Interactions =  mc.Contains("interactions") ? x.Sum(y => y.Interactions)    : null,
            //         Clicks =        mc.Contains("clicks") ? x.Sum(y => y.Clicks)                : null,
            //         UniqueUsers =   mc.Contains("uniqueUsers") ? x.Sum(y => y.UniqueUsers)      : null,

            //         Pinches =       mc.Contains("pinches") ? x.Sum(y => y.Pinches)              : null,
            //         Touches =       mc.Contains("touches") ? x.Sum(y => y.Touches)              : null,
            //         Swipes =        mc.Contains("swipes") ? x.Sum(y => y.Swipes)                : null,
            //     })
            //     .ToList();

            // return Ok(d);

            return null;
        }

        // /// <summary>
        // /// Campaign overview
        // /// </summary>
        // /// <param name="id">Campaign id</param>
        // [HttpGet("{id:int}/overview")]
        // public async Task<ActionResult<AggDaily>> GetOverview(uint id)
        // {
        //     throw new NotImplementedException("TODO");
        // }

        // /// <summary>
        // /// Campaign ads totals
        // /// </summary>
        // /// <param name="id">Campaign id</param>
        // /// <param name="m">Selected metrics, override default metrics</param>
        // [HttpGet("{id:int}/overview/ads/{m?}")]
        // public async Task<ActionResult<AggDaily>> GetOverviewAds(uint id, string m = "campaignName,adName,impressions,interactions,clicks,uniqueUsers")
        // {
        //     var mc = m.Split(',');

        //     var data = await _aggDaily
        //         .Where(x => x.CampaignId == id)
        //         .GroupBy(x => x.AdId)
        //         .Select(x => new AggDaily
        //         {
        //             AdId = x.First().AdId,
                    
        //             AdName =        mc.Contains("adName") ? x.First().AdName                    : null,
        //             Impressions =   mc.Contains("impressions") ? x.Sum(y => y.Impressions)      : null,
        //             Interactions =  mc.Contains("interactions") ? x.Sum(y => y.Interactions)    : null,
        //             Clicks =        mc.Contains("clicks") ? x.Sum(y => y.Clicks)                : null,
        //             UniqueUsers =   mc.Contains("uniqueUsers") ? x.Sum(y => y.UniqueUsers)      : null,

        //             Pinches =       mc.Contains("pinches") ? x.Sum(y => y.Pinches)              : null,
        //             Touches =       mc.Contains("touches") ? x.Sum(y => y.Touches)              : null,
        //             Swipes =        mc.Contains("swipes") ? x.Sum(y => y.Swipes)                : null,
        //         })
        //         .ToListAsync();

        //     return Ok(data);
        // }
    }
}
