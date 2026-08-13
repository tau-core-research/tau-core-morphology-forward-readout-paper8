#!/usr/bin/env python3
"""Acquire and freeze public PHANGS MUSE H-alpha and ALMA CO fields."""

from __future__ import annotations

import hashlib
import json
import argparse
import urllib.request
from pathlib import Path

from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
NGC3351_SOURCES = {
    "NGC3351_MAPS_copt_1.05asec.fits": (
        "https://dataportal.eso.org/dataPortal/file/ADP.2021-07-16T10:20:56.458",
        "c67e284f4556f6a9e5e74270c2076d37a2a9fb29563ceb10b95ae2dbae9b88bf",
    ),
    "group.uid___A001_X2fb_X27c.lp_schinner.ngc3351_12m7mtp_co21_mom1wprior.fits": (
        "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X27c.lp_schinner/group.uid___A001_X2fb_X27c.lp_schinner.ngc3351_12m7mtp_co21_mom1wprior.fits",
        "59f9c5e2c9d94ffae72986ecd3993c9808e9bc3caab81c32cbfd870c60669e74",
    ),
    "group.uid___A001_X2fb_X27c.lp_schinner.ngc3351_12m7mtp_co21_emom1wprior.fits": (
        "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X27c.lp_schinner/group.uid___A001_X2fb_X27c.lp_schinner.ngc3351_12m7mtp_co21_emom1wprior.fits",
        "69fd5f32a915caed7859f9e38c3c33f20690d9f3380bff13ff5a2c97bf5214f9",
    ),
    "group.uid___A001_X2fb_X27c.lp_schinner.ngc3351_12m7mtp_co21_broad_mom0.fits": (
        "https://almascience.nrao.edu/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X27c.lp_schinner/group.uid___A001_X2fb_X27c.lp_schinner.ngc3351_12m7mtp_co21_broad_mom0.fits",
        "4da8ade899be0fd2742ec5b6a8fea5b48a62b5a1cc57e040b64a0bdd5be294cc",
    ),
}
CONFIGS = {
    "NGC3351": {"slug": "ngc3351", "psf": 1.05, "sources": NGC3351_SOURCES},
    "NGC4254": {
        "slug": "ngc4254", "psf": 0.89,
        "sources": {
            "NGC4254_MAPS_copt_0.89asec.fits": (
                "https://dataportal.eso.org/dataPortal/file/ADP.2021-07-16T10:20:56.482",
                "6c04947a4d575233517526257374934fbf3b931c9d5451760653d4a8a1b181d8",
            ),
            "group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_mom1wprior.fits": (
                "https://almascience.nrao.edu/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X29a.lp_schinner/group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_mom1wprior.fits",
                "e18c06000af4b56e3ecf9c731022b0a7261d742515c49ff63ee9a550cf5c62e6",
            ),
            "group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_emom1wprior.fits": (
                "https://almascience.nrao.edu/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X29a.lp_schinner/group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_emom1wprior.fits",
                "5df8232ade40755522cbef08816b87e2c8dad4d310b5600a349bddb0450d1cea",
            ),
            "group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_broad_mom0.fits": (
                "https://almascience.nrao.edu/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X29a.lp_schinner/group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_broad_mom0.fits",
                "ba6fbc147029ef030a4bc2b63893f7141b0c2ce7453a0edc8b548dc850888c9b",
            ),
        },
    },
    "NGC3627": {
        "slug": "ngc3627", "psf": 1.05,
        "source_side_selection": {
            "role": "independent morphology-complex stress-control replication",
            "rule": "public matched PHANGS-MUSE/ALMA fields, moderate inclination, and source-known bar plus interaction; selected without tracer contrast or rotation residual",
            "muse_release": "https://www.eso.org/sci/publications/announcements/sciann17425.html",
            "alma_release": "https://arxiv.org/abs/2104.07739",
        },
        "sources": {
            "NGC3627_MAPS_copt_1.05asec.fits": (
                "https://dataportal.eso.org/dataPortal/file/ADP.2021-07-16T10:20:56.470",
                "baa454dbda4bdf46b8dd4fbee1da1741c4aa04f6c3531cde252da4a8c1bd125d",
            ),
            "group.uid___A001_X2fb_X286.lp_schinner.ngc3627_12m7mtp_co21_mom1wprior.fits": (
                "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X286.lp_schinner/group.uid___A001_X2fb_X286.lp_schinner.ngc3627_12m7mtp_co21_mom1wprior.fits",
                "5eb99c32ff578486df5dc563e1e66f470c55e0f1dff05b413b71763d08856e70",
            ),
            "group.uid___A001_X2fb_X286.lp_schinner.ngc3627_12m7mtp_co21_emom1wprior.fits": (
                "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X286.lp_schinner/group.uid___A001_X2fb_X286.lp_schinner.ngc3627_12m7mtp_co21_emom1wprior.fits",
                "582858cb729139409dca7d8bd3b294ed9298351904aebd3ec0693f7a92afc824",
            ),
            "group.uid___A001_X2fb_X286.lp_schinner.ngc3627_12m7mtp_co21_broad_mom0.fits": (
                "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X286.lp_schinner/group.uid___A001_X2fb_X286.lp_schinner.ngc3627_12m7mtp_co21_broad_mom0.fits",
                "ec4640ce1d7b94f3c437338992981ff5cb29a3553a9fdc2e33d539aa7c4484b7",
            ),
        },
    },
    "NGC4535": {
        "slug": "ngc4535", "psf": 0.56,
        "source_side_selection": {
            "role": "independent barred-galaxy morphology-orthogonal replication",
            "rule": "public matched PHANGS-MUSE/ALMA fields, moderate inclination, source-known bar, and no prefrozen m1 nuisance label; selected without tracer contrast or rotation residual",
            "muse_release": "https://www.eso.org/sci/publications/announcements/sciann17425.html",
            "alma_release": "https://arxiv.org/abs/2104.07739",
        },
        "sources": {
            "NGC4535_MAPS_copt_0.56asec.fits": (
                "https://dataportal.eso.org/dataPortal/file/ADP.2021-07-16T10:20:56.518",
                "cfa4530d8db9e70aa9f2b50ed2e9261c11c382c5809d3eafe92ea826743dc68f",
            ),
            "group.uid___A001_X2fb_X2cc.lp_schinner.ngc4535_12m7mtp_co21_mom1wprior.fits": (
                "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X2cc.lp_schinner/group.uid___A001_X2fb_X2cc.lp_schinner.ngc4535_12m7mtp_co21_mom1wprior.fits",
                "45889fcc280b2738909ad5637d92ba95a3092cf48bfc82e38c0d32f0efd48dff",
            ),
            "group.uid___A001_X2fb_X2cc.lp_schinner.ngc4535_12m7mtp_co21_emom1wprior.fits": (
                "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X2cc.lp_schinner/group.uid___A001_X2fb_X2cc.lp_schinner.ngc4535_12m7mtp_co21_emom1wprior.fits",
                "95f8c6a00d7ba9fb70a3a4e601b10dca8a927646bb1ec602cfce6d0d058cb2c2",
            ),
            "group.uid___A001_X2fb_X2cc.lp_schinner.ngc4535_12m7mtp_co21_broad_mom0.fits": (
                "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X2cc.lp_schinner/group.uid___A001_X2fb_X2cc.lp_schinner.ngc4535_12m7mtp_co21_broad_mom0.fits",
                "133f7b2cddb38948f2ee6c973fd909b7ea2f83e27251ae737804a3cd984c30dd",
            ),
        },
    },
    "IC5332": {
        "slug": "ic5332", "psf": 0.87,
        "source_side_selection": {
            "role": "preregistered confirmatory population endpoint",
            "rule": "25<=inclination<=70 deg, S4G decomposition present, BAR absent; selected before tracer contrast was opened",
            "muse_release": "https://www.eso.org/sci/publications/announcements/sciann17425.html",
            "alma_release": "https://arxiv.org/abs/2104.07739",
        },
        "sources": {
            "IC5332_MAPS_copt_0.87asec.fits": (
                "https://dataportal.eso.org/dataPortal/file/ADP.2021-07-16T10:20:56.326",
                "c620c2bbc9dbd9655a40ceb5290d461e50ba8fb9d1da26c912a9a0151fe55e1a",
            ),
            "group.uid___A001_X2fe_X2bb.lp_schinner.ic5332_12m7mtp_co21_mom1wprior.fits": (
                "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fe_X2bb.lp_schinner/group.uid___A001_X2fe_X2bb.lp_schinner.ic5332_12m7mtp_co21_mom1wprior.fits",
                "3cbaa8506ecc9ed9ec2e9b8fe725a6b6ab8e4529ac7f9fd52dfc5d5c0ba9c110",
            ),
            "group.uid___A001_X2fe_X2bb.lp_schinner.ic5332_12m7mtp_co21_emom1wprior.fits": (
                "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fe_X2bb.lp_schinner/group.uid___A001_X2fe_X2bb.lp_schinner.ic5332_12m7mtp_co21_emom1wprior.fits",
                "16bcc923101e232e33c91fada2d8e0642d5c03f6ecbe30e6223c0097006b358b",
            ),
            "group.uid___A001_X2fe_X2bb.lp_schinner.ic5332_12m7mtp_co21_broad_mom0.fits": (
                "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fe_X2bb.lp_schinner/group.uid___A001_X2fe_X2bb.lp_schinner.ic5332_12m7mtp_co21_broad_mom0.fits",
                "bafbc1a3951842377e8575b59417c7b9c1daa45f4fab92520d8e554169745497",
            ),
        },
    },
    "NGC4321": {
        "slug": "ngc4321", "psf": 1.16,
        "source_side_selection": {
            "role": "preregistered confirmatory population endpoint",
            "rule": "25<=inclination<=70 deg, S4G decomposition present, BAR absent; selected before tracer contrast was opened",
            "alma_duplicate_rule": "X2b8 and X2c2 science arrays are identical; lexicographically first X2b8 group frozen",
            "muse_release": "https://www.eso.org/sci/publications/announcements/sciann17425.html",
            "alma_release": "https://arxiv.org/abs/2104.07739",
        },
        "sources": {
            "NGC4321_MAPS_copt_1.16asec.fits": (
                "https://dataportal.eso.org/dataPortal/file/ADP.2021-07-16T10:20:56.506",
                "7829e009cac7466716a6fb6edbe892a1ad28f15a3a91de2fe50d49576ef91b1b",
            ),
            "group.uid___A001_X2fb_X2b8.lp_schinner.ngc4321_12m7mtp_co21_mom1wprior.fits": (
                "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X2b8.lp_schinner/group.uid___A001_X2fb_X2b8.lp_schinner.ngc4321_12m7mtp_co21_mom1wprior.fits",
                "e4537cc40f9f893c2cefaf7fb4e5b6354a11619869fadfcfe2fe2aef9a52a7a1",
            ),
            "group.uid___A001_X2fb_X2b8.lp_schinner.ngc4321_12m7mtp_co21_emom1wprior.fits": (
                "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X2b8.lp_schinner/group.uid___A001_X2fb_X2b8.lp_schinner.ngc4321_12m7mtp_co21_emom1wprior.fits",
                "d456eb86989fa3b945a10c4e6d6ca1978d0256d767093daf0f562985a6bada54",
            ),
            "group.uid___A001_X2fb_X2b8.lp_schinner.ngc4321_12m7mtp_co21_broad_mom0.fits": (
                "https://almascience.eso.org/almadata/lp/PHANGS/phangs_groups/group.uid___A001_X2fb_X2b8.lp_schinner/group.uid___A001_X2fb_X2b8.lp_schinner.ngc4321_12m7mtp_co21_broad_mom0.fits",
                "3bc450f262a3024cb5e6b94f32dff404f9919e208b7a0442981a0ba2cb43897d",
            ),
        },
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--galaxy", choices=CONFIGS, default="NGC3351")
    args = parser.parse_args()
    galaxy = args.galaxy
    config = CONFIGS[galaxy]
    slug = config["slug"]
    out = ROOT / f"data/external/literature/{slug}_phangs_tracer_velocity"
    out.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, (url, expected) in config["sources"].items():
        path = out / name
        if not path.exists():
            urllib.request.urlretrieve(url, path)
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"Source hash changed for {name}: {actual}")
        manifest.append({"filename": name, "url": url, "sha256": actual, "bytes": path.stat().st_size})

    maps_name = next(name for name in config["sources"] if "MAPS_copt" in name)
    maps = out / maps_name
    with fits.open(maps, memmap=True) as hdus:
        required = ["HA6562_FLUX", "HA6562_FLUX_ERR", "HA6562_VEL", "HA6562_VEL_ERR"]
        if any(name not in hdus for name in required):
            raise RuntimeError("Required H-alpha MAPS extensions are absent")
        muse_shape = list(hdus["HA6562_VEL"].data.shape)
    co_name = next(name for name in config["sources"] if "_mom1wprior.fits" in name)
    co = out / co_name
    with fits.open(co, memmap=True) as hdus:
        header = hdus[0].header
        co_shape = list(hdus[0].data.shape)
        beam = [float(header["BMAJ"]) * 3600, float(header["BMIN"]) * 3600]

    result = {
        "schema": f"{slug}_phangs_tracer_velocity_fields_v01",
        "status": "SOURCE_NATIVE_2D_TRACER_VELOCITY_FIELDS_ACQUIRED",
        "galaxy": galaxy,
        "tracers": ["PHANGS-MUSE H-alpha", "PHANGS-ALMA CO(2-1)"],
        "muse_psf_fwhm_arcsec": config["psf"],
        "co_beam_fwhm_arcsec": beam,
        "muse_shape": muse_shape,
        "co_shape": co_shape,
        "manifest": manifest,
        "source_side_selection": config.get("source_side_selection"),
        "construction_uses_rotation_residual": False,
        "claim_boundary": "source-native 2D field acquisition and integrity freeze; no tracer innovation or Tau-channel result",
    }
    (DATA / f"{slug}_phangs_tracer_velocity_fields_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
