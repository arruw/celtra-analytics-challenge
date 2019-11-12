using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Data;
using MySql.Data.MySqlClient;
using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations.Schema;

namespace impression_rest_api
{
    [Table("agg_daily")]
    public class AggDaily
    {
        [Column("date")]
        public DateTime? Date { get; set; }

        [Column("campaign_id")]
        public uint? CampaignId { get; set; }

        [Column("ad_id")]
        public uint? AdId { get; set; }
        
        [Column("campaign_name")]
        public string CampaignName { get; set; }

        [Column("ad_name")]
        public string AdName { get; set; }

        [Column("impressions")]
        public long? Impressions { get; set; }

        [Column("clicks")]
        public long? Clicks { get; set; }

        [Column("swipes")]
        public long? Swipes { get; set; }

        [Column("pinches")]
        public long? Pinches { get; set; }

        [Column("touches")]
        public long? Touches { get; set; }

        [Column("uniqueUsers")]
        public long? UniqueUsers { get; set; }

        [Column("interactions")]
        public long? Interactions { get; set; }
    }

    public class AggDailyContext : DbContext
    {
        public DbSet<AggDaily> AggDaily { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder) 
        {
            modelBuilder.Entity<AggDaily>()
                .HasKey(x => new {x.Date, x.CampaignId, x.AdId});
        }

        public AggDailyContext(DbContextOptions<AggDailyContext> options) : base(options) {}
    }
}
    