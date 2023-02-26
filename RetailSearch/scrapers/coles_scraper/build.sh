 #!/bin/bash
 name="coles_scraper_image"
 docker build . -t ${name}
 docker tag ${name} us.gcr.io/apeiros/${name}
 docker push us.gcr.io/apeiros/${name}