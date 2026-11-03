# Enterprise Containerization & Kubernetes Hosting

## 1. Docker Build & Local Run

Build the minimal, non-root container image:
```bash
make docker-build
```

Run in background mode (`-d`):
```bash
docker run -d -p 8080:8080 --name mcp-server mcp-starter-python:latest
```

Verify health endpoints:
```bash
curl http://localhost:8080/healthz
# {"status":"healthy","service":"mcp-server"}
```

View logs:
```bash
docker logs mcp-server
docker stop mcp-server && docker rm mcp-server
```

---

## 2. Kubernetes Deployment Specification

Sample Kubernetes manifest for deployment behind an internal Ingress or Apigee Hybrid routing:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: enterprise-mcp-server
  labels:
    app: mcp-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
      containers:
      - name: mcp-server
        image: <your-registry>/mcp-starter-python:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: PORT
          value: "8080"
        - name: HOST
          value: "0.0.0.0"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 15
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
---
apiVersion: v1
kind: Service
metadata:
  name: enterprise-mcp-server
spec:
  selector:
    app: mcp-server
  ports:
  - port: 80
    targetPort: 8080
    name: http
  type: ClusterIP
```
