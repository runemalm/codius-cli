using OpenDDD.Infrastructure.Persistence.OpenDdd.DatabaseSession.Postgres;
using OpenDDD.Infrastructure.Repository.OpenDdd.Postgres;
using OpenDDD.Infrastructure.Persistence.Serializers;
using OpenDDD.Domain.Model.Exception;
using Bookstore.Domain.Model;

namespace Bookstore.Infrastructure.Repositories.OpenDdd.Postgres
{
    public class PostgresOpenDddCustomerRepository : PostgresOpenDddRepository<Customer, Guid>, ICustomerRepository
    {
        private readonly ILogger<PostgresOpenDddCustomerRepository> _logger;

        public PostgresOpenDddCustomerRepository(
            PostgresDatabaseSession session, 
            IAggregateSerializer serializer, 
            ILogger<PostgresOpenDddCustomerRepository> logger) 
            : base(session, serializer)
        {
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }

        // Implement any additional domain-specific methods from ICustomerRepository here
    }
}
