#!/usr/bin/env fish

begin
    set -l IFS
    set a (./conlleval < result/eng.testa)
    set b (./conlleval < result/eng.testb)
end

echo eng.testa
echo $a
echo eng.testb
echo $b
