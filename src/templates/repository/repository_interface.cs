using OpenDDD.Domain.Model;

namespace Bookstore.Domain.Model
{
    public interface ICustomerRepository : IRepository<Customer, Guid>
    {
        // Add any additional domain-specific query methods here
    }
}
