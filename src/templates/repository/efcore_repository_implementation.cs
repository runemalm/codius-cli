using Microsoft.EntityFrameworkCore;
using OpenDDD.Infrastructure.Persistence.UoW;
using OpenDDD.Infrastructure.Repository.EfCore;
using Bookstore.Domain.Model.Customer;

namespace Bookstore.Infrastructure.Repositories.EfCore
{
    public class EfCoreCustomerRepository : EfCoreRepository<Customer, Guid>, ICustomerRepository
    {
        private readonly ILogger<EfCoreCustomerRepository> _logger;

        public EfCoreCustomerRepository(IUnitOfWork unitOfWork, ILogger<EfCoreCustomerRepository> logger) 
            : base(unitOfWork)
        {
            _logger = logger;
        }

        // Implement any additional domain-specific methods from ICustomerRepository here
    }
}
