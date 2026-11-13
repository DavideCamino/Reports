// Run from this directory: root -l -b -q 'fit_space.C()'
// For an interactive canvas: root -l 'fit_space.C()'
// Optional input/output: root -l -b -q 'fit_space.C("space.csv", "space_fit")'

#include <Rtypes.h>
#include <TCanvas.h>
#include <TF1.h>
#include <TFitResultPtr.h>
#include <TGraph.h>
#include <TLegend.h>
#include <TObject.h>
#include <TString.h>
#include <TStyle.h>

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

void fit_space(const char *input = "space.csv", const char *output = "space_fit")
{
    std::ifstream file(input);
    if (!file) {
        std::cerr << "Cannot open " << input << '\n';
        return;
    }

    std::vector<double> x, y;
    std::string line;
    std::getline(file, line); // Skip the x,y header.
    while (std::getline(file, line)) {
        if (line.find_first_not_of(" \t\r") == std::string::npos)
            continue;
        std::replace(line.begin(), line.end(), ',', ' ');
        std::istringstream row(line);
        double xi, yi;
        if (!(row >> xi >> yi) || !std::isfinite(xi) || !std::isfinite(yi)) {
            std::cerr << "Invalid data row: " << line << '\n';
            return;
        }
        x.push_back(xi);
        y.push_back(yi);
    }
    if (x.size() < 3) {
        std::cerr << "At least three data points are required for a quadratic fit.\n";
        return;
    }

    gStyle->SetOptFit(0);
    gStyle->SetOptStat(0);
    auto *canvas = new TCanvas("space_canvas", "Space: quadratic fit", 1000, 750);
    canvas->SetGrid();
    canvas->SetLeftMargin(0.12);
    canvas->SetBottomMargin(0.12);

    auto *graph = new TGraph(static_cast<int>(x.size()), x.data(), y.data());
    graph->SetName("space_data");
    graph->SetTitle("Space cost;N. bits factors;N. gates");
    graph->SetMarkerStyle(20);
    graph->SetMarkerSize(1);
    graph->SetMarkerColor(kBlack);

    const auto range = std::minmax_element(x.begin(), x.end());
    // ROOT pol2 uses [0] + [1]*x + [2]*x*x: c=[0], b=[1], a=[2].
    auto *fit = new TF1("space_pol2", "pol2", *range.first, *range.second);
    fit->SetLineColor(kRed);
    //fit->SetLineWidth(3);
    fit->SetNpx(500);
    // S: return fit status; Q: quiet; R: use function range; N: draw manually.
    TFitResultPtr result = graph->Fit(fit, "N");
    if (static_cast<int>(result) != 0) {
        std::cerr << "Quadratic fit failed (status " << static_cast<int>(result) << ").\n";
        return;
    }

    const double a = fit->GetParameter(2);
    const double b = fit->GetParameter(1);
    const double c = fit->GetParameter(0);

    const double e_a = fit->GetParError(2);
    const double e_b = fit->GetParError(1);
    const double e_c = fit->GetParError(0);

    double mean = 0.0;
    for (double yi : y)
        mean += yi;
    mean /= y.size();

    double sse = 0.0, sst = 0.0;
    for (std::size_t i = 0; i < x.size(); ++i) {
        const double residual = y[i] - fit->Eval(x[i]);
        sse += residual * residual;
        sst += (y[i] - mean) * (y[i] - mean);
    }
    const bool definedR2 = sst > 0.0;
    const double r2 = definedR2 ? 1.0 - sse / sst : 0.0;

    graph->Draw("AP");
    fit->Draw("SAME");
    

    auto *legend = new TLegend(0.15, 0.55, 0.5, 0.88);
    legend->SetMargin(0.05);
    //legend->SetBorderSize(1);
    legend->SetFillColor(kWhite);
    // ROOT legend labels support TLatex markup (not raw LaTeX).
    legend->SetTextFont(132); // Times-like serif font for a LaTeX-style appearance.
    legend->SetTextSize(0.032);
    legend->AddEntry(static_cast<TObject *>(nullptr),
                     "#it{y} = #it{a}#it{x}^{2} + #it{b}#it{x} + #it{c}", "");
    legend->AddEntry(static_cast<TObject *>(nullptr), Form("#it{a} = %.4g #pm %.4g", a, e_a), "");
    legend->AddEntry(static_cast<TObject *>(nullptr), Form("#it{b} = %.4g #pm %.4g", b, e_b), "");
    legend->AddEntry(static_cast<TObject *>(nullptr), Form("#it{c} = %.4g #pm %.4g", c, e_c), "");
    legend->AddEntry(static_cast<TObject *>(nullptr),
                     definedR2 ? Form("#it{R}^{2} = %.8f", r2) : "#it{R}^{2} undefined (constant y)", "");
    legend->Draw();

    canvas->Update();
    canvas->SaveAs(Form("%s.pdf", output));
    canvas->SaveAs(Form("%s.png", output));

    std::cout << std::setprecision(10)
              << "Fit: y = a*x^2 + b*x + c\n"
              << "a = " << a << "\nb = " << b << "\nc = " << c << '\n';
    if (definedR2)
        std::cout << "R^2 = " << r2 << '\n';
    else
        std::cout << "R^2 is undefined (constant y).\n";
}
