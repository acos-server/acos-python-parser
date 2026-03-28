
curl -X POST http://127.0.0.1:13456/extract_concepts -H "Content-Type: application/json" -d '{"code_str":"import txt"}'
echo ''
curl -X POST http://127.0.0.1:13456/extract_concepts -H "Content-Type: application/json" -d '{"code_str":"import txt\ntest=1"}'
echo ''
curl -X POST http://127.0.0.1:13456/extract_concepts -H "Content-Type: application/json" -d '{"code_str":"s='hola'"}'
echo ''
curl -X POST http://127.0.0.1:13456/extract_concepts -H "Content-Type: application/json" -d '{"code_str":"s='hola'\ns[0:2]"}'
echo ''
curl --fail http://localhost:13457/_stcore/health
echo ''
