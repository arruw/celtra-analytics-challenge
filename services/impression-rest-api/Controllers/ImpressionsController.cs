using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace impression_rest_api.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ImpressionsController : ControllerBase
    {
        private readonly ILogger<ImpressionsController> _logger;
        private readonly AggDailyContext _context;

        public ImpressionsController(ILogger<ImpressionsController> logger, AggDailyContext context)
        {
            _logger = logger;
            _context = context;
        }

        [HttpGet]
        public IActionResult GetCampaign(long? campaignId)
        {
            var query = _context.AggDaily.AsQueryable();

            if(campaignId.HasValue)
                query = query.Where(x => x.CampaignId == campaignId.Value);
                
            return Ok(query
                .GroupBy(x => new {x.Date, x.AdId})
                .OrderBy(x => x.Key.Date));
        }
    }
}
