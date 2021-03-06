from edibles.models.create_model import createCont
from edibles.utils.edibles_spectrum import EdiblesSpectrum
from edibles.models.model import Sightline
from edibles.fitter import fit


def testAdvancedFit(
    filename1="tests/HD170740_w860_redl_20140915_O12.fits",
    filename2="tests/HD148937_w346_blue_20150817_O11.fits",
):

    star_name = "HD170740"
    xmin = 7661.0
    xmax = 7670.0
    sp = EdiblesSpectrum(filename1, noDATADIR=True)
    subset = sp.getSpectrum(xmin, xmax)
    data = (subset["wave"], subset["flux"])

    # Cont parameters
    n_points = 4
    cont = createCont(data, n_points)

    slightline = Sightline(star_name=star_name, cont=cont)

    slightline.addSource(source_name="Telluric", b=1.07, d=0.046)
    slightline.addLine(name="tell_1", lam_0=7664.8, tau_0=0.75)
    slightline.addLine(name="tell_2", lam_0=7666, tau_0=0.75)

    slightline.addSource(source_name="Interstellar", b=1.0, d=0.001)
    slightline.addLine(name="KI_1", lam_0=7665.3, tau_0=0.1)
    slightline.addLine(name="KI_2", lam_0=7665.35, tau_0=0.05)

    fit_model = fit(star_name, data, slightline.model, silent=True)

    star = "HD148937"
    subset2 = EdiblesSpectrum(filename2, noDATADIR=True).getSpectrum(3301.5, 3304)
    data2 = (subset2["wave"], subset2["flux"])

    cont = createCont(data2, n_points=3)
    slightline2 = Sightline(star_name=star, cont=cont)
    slightline2.addSource("Source 1", 1.42631e-07, 0.036356)
    slightline2.addLine("NaI_1", lam_0=3302.46, tau_0=0.06)
    slightline2.addLine("NaI_2", lam_0=3303.1, tau_0=0.03)

    slightline2.dupSource("Source 1", "Source 2", 1.00005)
    slightline2.dupSource("Source 1", "Source 3", 0.99995)

    fit_model2 = fit(star, data2, slightline2.model, silent=True)

    return fit_model, fit_model2


if __name__ == "__main__":
    fit_model, fit_model2 = testAdvancedFit(
        filename1="HD170740_w860_redl_20140915_O12.fits",
        filename2="HD148937_w346_blue_20150817_O11.fits",
    )
    print(fit_model)
    print(fit_model2)
