import pytest

from infrastructure.services.openddd_convention_service import OpenDddConventionService
from infrastructure.services.tree_sitter_service import TreeSitterService


@pytest.fixture
def convention_service():
    service = OpenDddConventionService(TreeSitterService())
    return service


def test_format_class_code_removes_extra_blank_lines(convention_service):
    source = """\
using System;


namespace MyApp
{


    public class Invoice
    {

        public decimal Total { get; set; }



        public void RegisterPayment() {}



        public decimal CalculateBalance()
        {
            return Total - 5;
        }

    }

}"""
    expected = """\
using System;

namespace MyApp
{
    public class Invoice
    {
        public decimal Total { get; set; }

        public void RegisterPayment() {}

        public decimal CalculateBalance()
        {
            return Total - 5;
        }
    }
}
"""
    formatted = convention_service.format_class_code(source)
    assert formatted == expected


def test_format_class_code_trims_trailing_whitespace(convention_service):
    source = """\
public class Example   
{
    public int Value { get; set; }    

    public void Method() { }    
}    
"""
    expected = """\
public class Example
{
    public int Value { get; set; }

    public void Method() { }
}
"""
    formatted = convention_service.format_class_code(source)
    assert formatted == expected


def test_format_class_code_ends_with_newline(convention_service):
    source = """\
public class SingleMethod
{
    public void X() {}
}"""
    expected = """\
public class SingleMethod
{
    public void X() {}
}
"""
    formatted = convention_service.format_class_code(source)
    assert formatted.endswith("\n")
    assert formatted == expected


def test_format_class_code_adds_property_to_empty_class(convention_service):
    source = """\
using System;

namespace MyApp.Domain.Model.Invoice
{
    public class Invoice
    {
        public int Amount { get; set; }
        
    }
}
"""
    expected = """\
using System;

namespace MyApp.Domain.Model.Invoice
{
    public class Invoice
    {
        public int Amount { get; set; }
    }
}
"""

    formatted = convention_service.format_class_code(source)
    assert formatted == expected


def test_format_class_code_with_messy_source(convention_service):
    source = """\
﻿using OpenDDD.Domain.Model.Base;
using System;

namespace Orientera.Domain.Model.Person
{
    public class Person : AggregateRootBase<Guid>
    {
            public string Nickname { get; set; }

    private Person() { }  // Needed if persistence provider is EF Core..


        public static Person Create()
        {
            return new Person(Guid.NewGuid());
        }

        public void ChangeNickname(string newNickname)
        {
            // Implementation to change the nickname
        }
    }
}
"""
    expected = """\
using OpenDDD.Domain.Model.Base;
using System;

namespace Orientera.Domain.Model.Person
{
    public class Person : AggregateRootBase<Guid>
    {
        public string Nickname { get; set; }

        private Person() { }  // Needed if persistence provider is EF Core..

        public static Person Create()
        {
            return new Person(Guid.NewGuid());
        }

        public void ChangeNickname(string newNickname)
        {
            // Implementation to change the nickname
        }
    }
}
"""

    formatted = convention_service.format_class_code(source)
    assert formatted == expected


def test_format_class_code_ensures_one_newline_between_usings_and_namespace(convention_service):
    source = """\
using System;
using System.Linq;
namespace MyApp.Domain.Model
{
    public class Invoice
    {
        public decimal Total { get; set; }
    }
}
"""

    expected = """\
using System;
using System.Linq;

namespace MyApp.Domain.Model
{
    public class Invoice
    {
        public decimal Total { get; set; }
    }
}
"""

    formatted = convention_service.format_class_code(source)
    assert formatted == expected
