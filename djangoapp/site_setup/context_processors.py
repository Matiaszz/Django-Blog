from site_setup.models import SiteSetup


def cont_processor_example(req):
    return {'example': 'veio do processor (example)'}


def site_setup(request):
    setup = SiteSetup.objects.order_by('-id').first()

    return {
        'site_setup': setup
    }
