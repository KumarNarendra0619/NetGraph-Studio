# Deploy NetGraph Studio from GitHub to a public web app

## Recommended deployment

Use **Streamlit Community Cloud** for the first public deployment. GitHub remains the source repository and Streamlit Community Cloud runs `app.py` as the web application.

GitHub Pages is **not** the right deployment target because NetGraph Studio is a Python/Streamlit application and needs a Python runtime.

## Repository requirements

The repository already contains:

- `app.py` — Streamlit entrypoint
- `requirements.txt` — pinned City2Graph dependency and runtime dependencies
- `.streamlit/config.toml` — application theme/server settings
- `.github/workflows/tests.yml` — automated tests

The production dependency is pinned to `city2graph==1.0.0` so the web app stays aligned with the audited upstream API.

## First deployment

1. Open https://share.streamlit.io/ and sign in with the GitHub account that can access `KumarNarendra0619/NetGraph-Studio`.
2. Choose **Create app**.
3. Select repository: `KumarNarendra0619/NetGraph-Studio`.
4. Select branch: `main`.
5. Set the main file to: `app.py`.
6. Choose Python 3.12 if the deployment UI asks for a Python version.
7. Click **Deploy**.

The service will install `requirements.txt`, start Streamlit, and provide a public `*.streamlit.app` URL.

## After deployment

Open the public URL in a normal browser. A non-coder should be able to:

1. Choose a workflow from the sidebar.
2. Upload a supported spatial file.
3. Select a graph method.
4. Set parameters with controls rather than Python code.
5. Click the Run button.
6. Inspect node/edge statistics and the map/data tabs.
7. Download GeoJSON/CSV/GraphML/GML/edge-list and the reproducibility JSON record.

## Recommended first public test

Start with **Proximity / Contiguity → KNN** and a small GeoJSON point layer in a projected CRS. Use `k=5` and compare the node/edge result with the repository fidelity tests.

Then test, in order:

- Delaunay
- Gabriel
- RNG
- MST
- Radius
- Waxman
- Queen/Rook contiguity
- OD
- GTFS
- Urban Morphology

## Important scientific constraint

The web UI does not replace City2Graph algorithms. NetGraph Studio validates inputs, collects parameters, calls the original City2Graph public API, and presents/exports its result.

## If deployment fails

Open the deployment logs and identify the first Python/package error. Do not change multiple dependencies at once. Fix the first reproducible error, commit it to GitHub, and let the deployment rebuild.

## Update cycle

After the first deployment, every push to `main` can trigger a new deployment build. Keep GitHub Actions green before accepting a production-facing change.
