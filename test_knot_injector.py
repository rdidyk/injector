import pytest
import knot_injector


class TestInjector(object):

    @pytest.fixture()
    def provider(self):
        def test_provider(container=None):
            return {'name': 'test'}
        return test_provider

    @pytest.fixture()
    def container(self):
        return knot_injector.Container()

    def test_adding_service(self, container, provider):
        container.service()(provider)
        assert container.provide('test_provider')() == {'name': 'test'}

    def test_adding_factory(self, container, provider):
        container.factory()(provider)
        assert container.provide('test_provider')() == {'name': 'test'}

    def test_adding_non_unique_provider(self, container, provider):
        container.service()(provider)
        with pytest.raises(AttributeError) as ex:
            container.service()(provider)
            assert str(ex) == 'Provider name must be unique'

    def test_non_callable_provider(self, container):
        import random
        container.factory(name='test_prov')(random)
        assert container('test_prov') == random

    def test_injection(self, container, provider):
        import random
        container.service(name='test_provider')(provider)
        container.factory(name='rnd')(random)

        @container.inject
        def test_func(test_provider, rnd, msg, **kwargs):
            return test_provider, rnd, msg, kwargs

        res = test_func(msg="don't obey", answer=42)

        assert res == (
            {'name': 'test'},
            random,
            "don't obey",
            {'answer': 42},
        )
