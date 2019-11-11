using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Data;
using MySql.Data.MySqlClient;
using Microsoft.EntityFrameworkCore;

namespace impression_rest_api
{
    public class AggDaily
    {
        public DateTime Date { get; set; }

        public long CampaignId { get; set; }

        public long AdId { get; set; }
        
        public string CampaignName { get; set; }

        public string AdName { get; set; }

        public long Impressions { get; set; }

        public long Clicks { get; set; }

        public long Swipes { get; set; }

        public long Pinches { get; set; }

        public long Touches { get; set; }

        public long UniqueUsers { get; set; }

        public long Interactions { get; set; }
    }

    public class AggDailyContext : DbContext
    {
        public DbSet<AggDaily> AggDaily { get; set; }

        public AggDailyContext(DbContextOptions<AggDailyContext> options) : base(options) {}
    }
}
    