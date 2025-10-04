# from openfabric_pysdk.starter import Starter
from main import app

if __name__ == '__main__':
    # Starter.ignite(debug=False, host="0.0.0.0", port=5500)
    app.run(debug=False, host="0.0.0.0", port=5500)