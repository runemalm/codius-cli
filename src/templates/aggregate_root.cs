using OpenDDD.Domain.Model.Base;

namespace Bookstore.Domain.Model
{
    public class Customer : AggregateRootBase<Guid>
    {
        public string Name { get; private set; }

        private Customer() { }  // Needed if persistence provider is EF Core..

        private Customer(Guid id, string name) : base(id)
        {
            Name = name;
        }

        public static Customer Create(string name, string email)
        {
            return new Customer(Guid.NewGuid(), name);
        }

        public void ChangeName(string name)
        {
            Name = name;
        }
    }
}
